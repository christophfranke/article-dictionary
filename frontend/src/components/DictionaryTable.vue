<script setup lang="ts">
import { ref, computed, watchEffect, reactive } from 'vue';

import type { DictionaryView } from '@/dictionary/view';
import type { Word } from '@/types';

import { useProfile } from '@/use/user';

import useScroll from './dictionary-table/use-scroll';
import useSort from './dictionary-table/use-sort';

import Row from './dictionary-table/Row.vue'

import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Button from '@/elements/Button.vue';



const props = defineProps({
  dictionary: {
    type: Object as unknown as () => DictionaryView,
    required: true,
  },
  highlight: {
    type: String,
    default: '',
  },
  sort: {
    type: String,
    default: 'original',
  },
  display: {
    type: Object,
    default: {
      header: true,
      limit: 0,
      col: {
        number: false,
        original: true,
        translations: true,
        frequency: true,
        status: true,
        actions: true,
      },
      action: {
        known: true,
        ignore: true,
        add: true,
        sort: true,
        edit: true,
        retranslate: true,
        status: true,
        glosbe: true,
        detail: true,
      },
      behaviour: {
        highlight: true,
        scroll: true,
      }
    }
  }
});


useScroll(props);
const { sortTable, sortedWords } = useSort(props);
const profile = reactive(useProfile());

const highlightedWord = computed(() => {
  return (props.display.behaviour.highlight || props.display.behaviour.highlight)
    ? props.highlight.toLowerCase()
    : ''
}
);



const newWord = ref<string>('');
const addWord = async (): Promise<void> => {
  if (newWord.value) {
    await props.dictionary.addWord(newWord.value);
    newWord.value = '';
  }
};
</script>

<template>
  <div class="dictionary-table">
    <div v-if="display.action.add" class="add-word-section">
      <Label for="newWord">New Entry:</Label>
      <Input v-model="newWord" id="newWord" placeholder="Add word to dictionary" />
      <Button @click="addWord">Add</Button>
    </div>

    <table class="word-table">
      <thead>
        <tr v-if="display.header">
          <th
            @click="sortTable('number')"
            v-if="display.col.number"
            :title="display.action.sort ? 'Sort by appearence in text' : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >#
          </th>
          <th
            @click="sortTable('original')"
            v-if="display.col.original"
            :title="display.action.sort ? 'Sort by original word' : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >Original
          </th>
          <th
            @click="sortTable('translations')"
            v-if="display.col.translations"
            :title="display.action.sort ? 'Sort by translation' : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >Translations
          </th>
          <th
            @click="sortTable('frequency', 'desc')"
            v-if="display.col.frequency"
            :title="display.action.sort ? 'Sort by word frequency' : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >Frequency
          </th>
          <th
            @click="sortTable('status')"
            v-if="display.col.status"
            title="Sort by status">Status
          </th>
          <th v-if="display.col.actions" class="no-sort">Actions</th>
        </tr>
      </thead>
      <tbody>
        <Row v-for="(word) in sortedWords" :key="word.id" :word="word" :highlightedWord="highlightedWord" :display="props.display" :dictionary="props.dictionary" :profile="profile" />
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.add-word-section {
  margin-bottom: 20px;
}

.word-table {
  width: 100%;
  border-collapse: collapse;
}

th {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  cursor: pointer;
  background-color: #f2f2f2;
}

th:hover {
  background-color: #ddd;
}

th.no-sort {
  cursor: default;
}
th.no-sort:hover {
  background-color: #f2f2f2;
}

.add-word-section {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.add-word-section label {
  white-space: nowrap;
  flex-grow: 0;
}

.add-word-section input {
  flex-grow: 1;
  margin: 10px;
}

.add-word-section button {
  flex-grow: 0;
}
</style>
