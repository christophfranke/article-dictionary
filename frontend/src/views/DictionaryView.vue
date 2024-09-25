<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

import type { PartialWord } from '../types';
import type { DictionaryView } from '@/dictionary/view';

import DictionaryTable from '../components/DictionaryTable.vue';
import Statistics from '../components/Statistics.vue';

import { useDictionaryView } from '@/use/dictionary';

import Headline from '@/elements/Headline.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';

import __ from '@/i18n'


interface StatusFilters {
  new: boolean;
  seen: boolean;
  known: boolean;
  ignore: boolean;
}

const tableDisplayConfig = {
  header: true,
  limit: 200,
  sortBy: 'original',
  sortOrder: 'asc',
  col: {
    number: false,
    original: true,
    translations: true,
    status: true,
    lastSeen: true,
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

const filterFn = (word: PartialWord) => {
  if (!statusFilters.value[word.status]) {
    return false;
  }

  if (clusterOnly.value) {
    return word.clusterId == word.id
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

let isLoadingView: ref<boolean> | null = null
let dictionary: DictionaryView | null = null
const isLoading = computed(() => !isLoadingView || isLoadingView.value)
const isDictionaryReady = ref<boolean>(false)
const filter = ref<string>('');
const statusFilters = ref({
  new: true,
  seen: true,
  known: true,
  ignore: false,
} as { [key: string]: boolean });
const clusterOnly = ref(true)

onMounted(async () => {
  await new Promise(resolve => requestAnimationFrame(resolve))
  const view = useDictionaryView(filterFn);
  dictionary = view.dictionary
  isLoadingView = view.isLoading

  await new Promise(resolve => requestAnimationFrame(resolve))
  isDictionaryReady.value = true
  dictionary.load();
});
</script>

<template>
  <div class="dictionary-view">
    <Headline>{{ __('Dictionary View') }}</Headline>

    <p v-if="isLoading && !isDictionaryReady">
      {{ __('Loading dictionary...') }}
    </p>

    <template v-else>
      <div class="filter-section">
        <Label for="filter">{{ __('Filter:') }}</Label>
        <Input v-model="filter" id="filter" :placeholder="__('Search for...')" />
      </div>
      <Statistics :dictionary="dictionary!" class="statistics" v-if="isDictionaryReady" />

      <div class="status-filters">
        <Label for="newCheckbox">
          <Input id="newCheckbox" type="checkbox" v-model="statusFilters.new" />
          {{ __('New') }}
        </Label>

        <Label for="seenCheckbox">
          <Input id="seenCheckbox" type="checkbox" v-model="statusFilters.seen" />
          {{ __('Seen') }}
        </Label>

        <Label for="knownCheckbox">
          <Input id="knownCheckbox" type="checkbox" v-model="statusFilters.known" />
          {{ __('Known') }}
        </Label>

        <Label for="ignoreCheckbox">
          <Input id="ignoreCheckbox" type="checkbox" v-model="statusFilters.ignore" />
          {{ __('Ignore') }}
        </Label>

        <Label for="clustCheckbox">
          <Input id="clustCheckbox" type="checkbox" v-model="clusterOnly" />
          {{ __('Base Form') }}
        </Label>
      </div>

      <DictionaryTable :dictionary="dictionary!" :display="tableDisplayConfig" v-if="isDictionaryReady" />
    </template>
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
  white-space: nowrap;
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
