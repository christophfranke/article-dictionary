<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

import type { Word } from '../types';

import DictionaryTable from '../components/DictionaryTable.vue';
import Statistics from '../components/Statistics.vue';

import { useDictionaryView } from '@/use/dictionary';

import Headline from '@/elements/Headline.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';



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
    link: true,
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


const dictionary = useDictionaryView(filterFn);
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
</script>

<template>
  <div class="dictionary-view">
    <Headline>Dictionary View</Headline>

    <div class="filter-section">
      <Label for="filter">Filter:</Label>
      <Input v-model="filter" id="filter" placeholder="Search for..." />
    </div>
    <Statistics :dictionary="dictionary" class="statistics" />

    <div class="status-filters">
      <Label for="newCheckbox">
        <Input id="newCheckbox" type="checkbox" v-model="statusFilters.new" />
        New
      </Label>

      <Label for="seenCheckbox">
        <Input id="seenCheckbox" type="checkbox" v-model="statusFilters.seen" />
        Seen
      </Label>

      <Label for="knownCheckbox">
        <Input id="knownCheckbox" type="checkbox" v-model="statusFilters.known" />
        Known
      </Label>

      <Label for="ignoreCheckbox">
        <Input id="ignoreCheckbox" type="checkbox" v-model="statusFilters.ignore" />
        Ignore
      </Label>
    </div>

    <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" />
  </div>
</template>

<style scoped lang="scss">
.dictionary-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.filter-section {
  margin-bottom: 15px;
}

label {
  margin-bottom: 5px;
}

.status-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;

  label {
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  input {
    margin-right: 5px;
  }
}

.statistics {
  float: right;
  margin-left: 30px;
}
</style>
