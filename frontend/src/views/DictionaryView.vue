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
    <DictionaryTable :words="filteredWords" @update="updateWord" @add="addWord" />
    <button @click="resetDictionary">Reset and Rebuild Dictionary</button>
  </div>
</template>

<script setup lang="ts">
import DictionaryTable from '../components/DictionaryTable.vue';
import { ref, computed, onMounted } from 'vue';

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

const words = ref<Word[]>([]);
const filter = ref<string>('');
const statusFilters = ref({
  new: true,
  seen: true,
  known: true,
  ignore: false,
} as { [key: string]: boolean });

const filteredWords = computed<Word[]>(() => {
  let filtered: Word[] = words.value;

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

const loadDictionary = async (): Promise<void> => {
  const response = await fetch('/api/dictionary/');
  const wordsData: Word[] = await response.json();

  // Add index to each word in the array
  words.value = wordsData.map((word, index) => ({ ...word, index }));
};

const resetDictionary = async (): Promise<void> => {
  await fetch('/api/dictionary/reset', { method: 'POST' });
  loadDictionary();
};

const updateWord = (updatedWord: Word): void => {
  const index: number = words.value.findIndex((word) => word.original === updatedWord.original);
  if (index !== -1) {
    words.value[index] = updatedWord;
  }
};

const addWord = (newWord: Word): void => {
  words.value.push(newWord);  
}


onMounted(() => {
  loadDictionary();
});

</script>
