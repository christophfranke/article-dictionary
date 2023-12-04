<template>
  <div>
    <h1>Dictionary View</h1>
    <div>
      <label for="filter">Filter:</label>
      <input v-model="filter" id="filter" />
    </div>
    <div>
      <label for="newCheckbox">
        <input id="newCheckbox" type="checkbox" v-model="statusFilters.new" />
        New
      </label>

      <label for="seenCheckbox">
        <input id="seenCheckbox" type="checkbox" v-model="statusFilters.seen" />
        Seen
      </label>

      <label for="knownCheckbox">
        <input id="knownCheckbox" type="checkbox" v-model="statusFilters.known" />
        Known
      </label>

      <label for="ignoreCheckbox">
        <input id="ignoreCheckbox" type="checkbox" v-model="statusFilters.ignore" />
        Ignore
      </label>
    </div>
    <div>
      <label for="newWord">New Entry:</label>
      <input v-model="newWord" id="newWord" />
      <button @click="addWord">Add</button>
    </div>
    <table>
      <thead>
        <tr>
          <th @click="sortTable('original')">Original</th>
          <th @click="sortTable('translations')">Translations</th>
          <th @click="sortTable('status')">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(word) in filteredWords" :key="word.index">
          <td>{{ word.original }}</td>
          <td @click="editTranslations(word.index)" v-if="word.index !== editingTranslationIndex">
            {{ word.translations.join(', ') }}
          </td>
          <td v-else>
            <form @submit="updateTranslation">
              <input ref="editTranslationsInput" v-model="editTranslationsValue" @blur="editTranslations(-1)" />
              <input type="submit" value="ok" />
            </form>
          </td>
          <td @click="changeStatus(word)">{{ word.status }}</td>
        </tr>
      </tbody>
    </table>
    <button @click="resetDictionary">Reset and Rebuild Dictionary</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

interface Word {
  index: number;
  original: string;
  translations: string[];
  status: string;
}

interface StatusFilters {
  new: boolean;
  seen: boolean;
  known: boolean;
  ignore: boolean;
}

const words = ref<Array<Word>>([]);
const filter = ref<string>('');
const sortOrder = ref<string>('asc');
const sortedBy = ref<string>('');
const newWord = ref<string>('');
const editingTranslationIndex = ref<number>(-1);
const editTranslationsValue = ref<string>('');
const editTranslationsInput = ref<HTMLInputElement[] | null>(null);
const statusFilters = ref({
  new: true,
  seen: true,
  known: true,
  ignore: false,
} as { [key: string]: boolean });


const resetDictionary = async (): Promise<void> => {
  await fetch('/api/dictionary/reset', { method: 'POST' });
  loadDictionary();
};

const sortTable = (column: string): void => {
  if (column === sortedBy.value) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortedBy.value = column;
    sortOrder.value = 'asc';
  }
};

const sortedWords = computed<Array<Word>>(() => {
  const sorted = [...words.value];
  if (sortedBy.value) {
    sorted.sort((a, b) => {
      const order = sortOrder.value === 'asc' ? 1 : -1;

      // Type assertion to let TypeScript know that the properties exist
      const propertyA = (a as any)[sortedBy.value];
      const propertyB = (b as any)[sortedBy.value];

      return propertyA > propertyB ? order : -order;
    });
  }
  return sorted;
});

const loadDictionary = async (): Promise<void> => {
  const response = await fetch('/api/dictionary/');
  const wordsData: Word[] = await response.json();

  // Add index to each word in the array
  words.value = wordsData.map((word, index) => ({ ...word, index }));
};

const filteredWords = computed<Word[]>(() => {
  let filtered: Word[] = sortedWords.value;

  filtered = filtered.filter((word) => {
    if (!statusFilters.value[word.status]) {
      return false;
    }

    if (filter.value) {
      return (
        word.original.toLowerCase().includes(filter.value.toLowerCase()) ||
        word.translations.some((t) => t.toLowerCase().includes(filter.value.toLowerCase())) ||
        word.status.toLowerCase().includes(filter.value.toLowerCase())
      );
    }

    return true;
  });

  return filtered;
});

const editTranslations = async (index: number): Promise<void> => {
  editingTranslationIndex.value = index;
  if (index !== -1) {
    const word: Word = words.value[index];
    editTranslationsValue.value = word.translations.join(', ');

    await new Promise((resolve) => setTimeout(resolve, 0));

    // Focus the input field for editing translations
    if (editTranslationsInput.value && editTranslationsInput.value.length > 0) {
      editTranslationsInput.value[0].focus();
      editTranslationsInput.value[0].select();
    }
  }
};

const updateTranslation = async (e: Event): Promise<void> => {
  e.preventDefault();
  const word: Word = words.value[editingTranslationIndex.value];
  const translations: string[] = editTranslationsValue.value.split(',').map((t) => t.trim());
  await updateWord(word.original, { translations });
  editingTranslationIndex.value = -1;
};

const changeStatus = async (word: Word): Promise<void> => {
  const statusOptions: string[] = ['new', 'seen', 'known', 'ignore'];
  const currentIndex: number = statusOptions.indexOf(word.status);
  const newIndex: number = (currentIndex + 1) % statusOptions.length;
  const newStatus: string = statusOptions[newIndex];

  await updateWord(word.original, { status: newStatus });
};

const addWord = async (): Promise<void> => {
  if (newWord.value) {
    const result = await fetch('/api/dictionary/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ original: newWord.value }),
    });

    if (result.ok) {
      const addedWord: Word = await result.json();
      words.value.push(addedWord);
    } else {
      console.log('Error adding word');
    }

    newWord.value = '';
  }
};

const updateWord = async (original: string, data: Record<string, unknown>): Promise<void> => {
  const result = await fetch(`/api/dictionary/update/${original}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (result.ok) {
    const updatedWord: Word = await result.json();
    const index: number = words.value.findIndex((word) => word.original === original);
    if (index !== -1) {
      words.value[index] = updatedWord;
    }
  } else {
    console.log('Error updating word');
  }
};

onMounted(() => {
  loadDictionary();
});
</script>
