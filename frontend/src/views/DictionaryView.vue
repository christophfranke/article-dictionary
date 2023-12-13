<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

import type { Word } from '../types';

import DictionaryTable from '../components/DictionaryTable.vue';
import Statistics from '../components/Statistics.vue';

import useDictionary from '@/use/dictionary';


interface StatusFilters {
  new: boolean;
  seen: boolean;
  known: boolean;
  ignore: boolean;
}

const tableDisplayConfig = {
  header: true,
  limit: 200,
  col: {
    number: false,
    original: true,
    translations: true,
    status: true,
    actions: true,
    frequency: true,
  },
  action: {
    known: true,
    ignore: true,
    add: true,
    sort: true,
    edit: true,
    status: true,
    retranslate: true,
    glosbe: true,
    detail: true,
  },
  behaviour: {
    highlight: true,
    scroll: true,
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


const dictionary = useDictionary([], filterFn);
const filter = ref<string>('');
const statusFilters = ref({
  new: true,
  seen: true,
  known: true,
  ignore: false,
} as { [key: string]: boolean });


const rebuildDictionary = async (): Promise<void> => {
  await dictionary.rebuild();
};

onMounted(async () => {
  await dictionary.load();
});

</script>

<template>
  <div class="dictionary-view">
    <h1>Dictionary View</h1>

    <div class="filter-section">
      <label for="filter">Filter:</label>
      <input v-model="filter" id="filter" placeholder="Search for..." />
    </div>
    <Statistics :dictionary="dictionary" class="statistics" />

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
  </div>
</template>

<style scoped>
.dictionary-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.filter-section {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.status-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.status-filters label {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #555;
}

.status-filters input {
  margin-right: 5px;
}

.DictionaryTable {
  margin-top: 20px;
}

.statistics {
  float: right;
  margin-left: 30px;
}
</style>
