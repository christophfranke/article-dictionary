<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

import type { Word } from '../types';

import DictionaryTable from '../components/DictionaryTable.vue';
import Statistics from '../components/Statistics.vue';

import createDictionaryCollection from '../dictionary/collection';
import * as DictionaryRequest from '../dictionary/request';


interface StatusFilters {
  new: boolean;
  seen: boolean;
  known: boolean;
  ignore: boolean;
}

const tableDisplayConfig = {
  header: true,
  col: {
    number: false,
    original: true,
    translations: true,
    status: true,
    actions: true,
  },
  action: {
    known: false,
    ignore: true,
    add: true,
    sort: true,
    edit: true,
    status: true,
    retranslate: true,
  }
};

const filterFn = (word: Word) => {
  if (!statusFilters.value[word.status]) {
    return false;
  }

  if (filter.value) {
    return (
      word.original.toLowerCase().includes(filter.value.toLowerCase()) ||
      word.translations.some((t: string) => t.toLowerCase().includes(filter.value.toLowerCase())) ||
      word.status.toLowerCase().includes(filter.value.toLowerCase())
    );
  }

  return true;
};


const dictionary = createDictionaryCollection([], filterFn);
const words = computed<Word[]>(() => dictionary.get());
const filter = ref<string>('');
const statusFilters = ref({
  new: true,
  seen: true,
  known: true,
  ignore: false,
} as { [key: string]: boolean });


const rebuildDictionary = async (): Promise<void> => {
  await DictionaryRequest.rebuild();
  await dictionary.load();
};

onMounted(async () => {
  await dictionary.load();
});

</script>

<template>
  <div class="dictionary-view">
    <h1>Dictionary View</h1>
    <Statistics :dictionary="dictionary" />

    <div class="filter-section">
      <label for="filter">Filter:</label>
      <input v-model="filter" id="filter" />
    </div>

    <div class="status-filters">
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

    <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" />

    <button class="rebuild-button" @click="rebuildDictionary">Drop and Rebuild Dictionary</button>
  </div>
</template>

<style scoped>
.dictionary-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #333;
  font-size: 2em;
  margin-bottom: 20px;
}

.filter-section {
  margin-bottom: 20px;
}

label {
  margin-right: 10px;
}

.input-field {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.status-filters {
  display: flex;
  margin-bottom: 20px;
}

.status-filters label {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.status-filters input {
  margin-right: 5px;
}

.rebuild-button {
  margin-top: 20px;
  background-color: #dc3545; /* Red background for danger */
  color: #fff;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.rebuild-button:hover {
  background-color: #c82333; /* Darker red for hover effect */
}

.statistics {
  float: right;
}
</style>
