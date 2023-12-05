<template>
  <div>
    <div v-if="props.updateWords">
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
        <tr v-for="(word) in sortedWords" :key="word.index">
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  words: {
    type: Array as unknown as () => Word[],
    required: true,
  },
  updateWords: {
    type: Function as unknown as () => (words: Word[]) => void,
    required: false,
  },
});

interface Word {
  index: number;
  original: string;
  translations: string[];
  status: string;
}

const newWord = ref<string>('');
const editingTranslationIndex = ref<number>(-1);
const editTranslationsValue = ref<string>('');
const editTranslationsInput = ref<HTMLInputElement[] | null>(null);

const sortOrder = ref<string>('asc');
const sortedBy = ref<string>('original');

const sortTable = (column: string): void => {
  if (column === sortedBy.value) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortedBy.value = column;
    sortOrder.value = 'asc';
  }
};

const sortedWords = computed<Array<Word>>(() => {
  const sorted = [...props.words];
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

const editTranslations = async (index: number): Promise<void> => {
  if (props.updateWords) {    
    editingTranslationIndex.value = index;
    if (index !== -1) {
      const word: Word | undefined = props.words.find((word) => word.index === index);

      if (word) {
        editTranslationsValue.value = word.translations.join(', ');

        await new Promise((resolve) => setTimeout(resolve, 0));

        // Focus the input field for editing translations
        if (editTranslationsInput.value && editTranslationsInput.value.length > 0) {
          editTranslationsInput.value[0].focus();
          editTranslationsInput.value[0].select();
        }
      }
    }
  }
};

const updateTranslation = async (e: Event): Promise<void> => {
  e.preventDefault();
  if (props.updateWords) {
    const word: Word | undefined = props.words.find((word) => word.index === editingTranslationIndex.value);

    if (word) {
      const translations: string[] = editTranslationsValue.value.split(',').map((t) => t.trim());
      await updateWord(word.original, { translations });
      editingTranslationIndex.value = -1;
    }
  }
};

const changeStatus = async (word: Word): Promise<void> => {
  const statusOptions: string[] = ['new', 'seen', 'known', 'ignore'];
  const currentIndex: number = statusOptions.indexOf(word.status);
  const newIndex: number = (currentIndex + 1) % statusOptions.length;
  const newStatus: string = statusOptions[newIndex];

  await updateWord(word.original, { status: newStatus });
};

const addWord = async (): Promise<void> => {
  if (props.updateWords && newWord.value) {
    const result = await fetch('/api/dictionary/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ original: newWord.value }),
    });

    if (result.ok) {
      const addedWord: Word = await result.json();
      props.updateWords([...props.words, {
        ...addedWord,
        index: props.words.length,
      }]);
    } else {
      console.log('Error adding word');
    }

    newWord.value = '';
  }
};

const updateWord = async (original: string, data: Record<string, unknown>): Promise<void> => {
  if (props.updateWords) {
    const result = await fetch(`/api/dictionary/update/${original}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (result.ok) {
      const updatedWord: Word = await result.json();
      const newWords: Word[] = [...props.words.map(word => word.original === updatedWord.original
        ? ({
          ...word,
          ...updatedWord
        }) : word
      )];
      props.updateWords(newWords);
    } else {
      console.log('Error updating word');
    }
  }
};
</script>
