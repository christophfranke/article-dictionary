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
    <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" />
    <button @click="resetDictionary">Reset and Rebuild Dictionary</button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import DictionaryTable from '../components/DictionaryTable.vue';
import createDictionaryCollection from '../services/dictionary-collection';

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

const tableDisplayConfig = {
  header: true,
  col: {
    original: true,
    translations: true,
    status: true,
    actions: false,
  },
  action: {
    known: true,
    ignore: true,
    add: true,
    sort: true,
    edit: true,
  }
};

const filterFn = (word) => {
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


const resetDictionary = async (): Promise<void> => {
  await DictionaryRequest.reset();
  await dictionary.load()
};

onMounted(async () => {
  await dictionary.load();
});

</script>
