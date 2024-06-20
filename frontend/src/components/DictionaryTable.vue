<script setup lang="ts">
import { ref, computed, watchEffect, reactive, onMounted } from 'vue';
import type { PropType } from 'vue';

import type { DictionaryView } from '@/dictionary/view';
import type { Word } from '@/types';

import { useProfile } from '@/use/user';

import useScroll from './dictionary-table/use-scroll';
import useSort from './dictionary-table/use-sort';

import Row from './dictionary-table/Row.vue'

import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Button from '@/elements/Button.vue';

import __ from '@/i18n'


const props = defineProps({
  dictionary: {
    type: Object as PropType<DictionaryView>,
    required: true,
  },
  highlight: {
    type: String,
    default: '',
  },
  display: {
    type: Object,
    default: {
      header: true,
      limit: 0,
      sortBy: 'original',
      sortOrder: 'asc',
      col: {
        number: false,
        original: true,
        translations: true,
        frequency: true,
        status: true,
        lastSeen: true,
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
const { profile } = useProfile();

const isReady = ref<boolean>(false)
const usedWords = computed(() => isReady.value ? sortedWords.value : [])
onMounted(async () => {
  await new Promise(resolve => requestAnimationFrame(resolve))
  isReady.value = true
})

const highlightedWord = computed(() => {
  return (props.display.behaviour.highlight || props.display.behaviour.highlight)
    ? props.highlight
    : ''
});

const isWordHighlighted = ref<{ [key: string]: boolean }>({});
const lastHighlightedWord = ref<string>('');
watchEffect(() => {
  if (props.display.behaviour.highlight) {
    const word = props.dictionary.find(highlightedWord.value);
    if (word) {
      if (lastHighlightedWord.value) {
        isWordHighlighted.value[lastHighlightedWord.value] = false;
      }
      isWordHighlighted.value[word.original] = true;
      lastHighlightedWord.value = word.original;
    } else {
      isWordHighlighted.value[lastHighlightedWord.value] = false;
      lastHighlightedWord.value = '';
    }
  } else {
    if (lastHighlightedWord.value) {
      isWordHighlighted.value[lastHighlightedWord.value] = false;
      lastHighlightedWord.value = '';    
    }
  }
});


const newWord = ref<string>('');
const addWord = async (): Promise<void> => {
  if (newWord.value) {
    await props.dictionary.add({ original: newWord.value });
    newWord.value = '';
  }
};
</script>

<template>
  <div class="dictionary-table">
    <div v-if="display.action.add" class="add-word-section">
      <Label for="newWord">{{ __('New Entry:') }}</Label>
      <Input v-model="newWord" id="newWord" :placeholder="__('Add word to dictionary')" />
      <Button @click="addWord">{{ __('Add') }}</Button>
    </div>

    <table class="word-table">
      <thead>
        <tr v-if="display.header">
          <th
            @click="sortTable('order')"
            v-if="display.col.number"
            :title="display.action.sort ? __('Sort by appearence in text') : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >#
          </th>
          <th
            @click="sortTable('original')"
            v-if="display.col.original"
            :title="display.action.sort ? __('Sort by original word') : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >{{ __('Original') }}
          </th>
          <th
            @click="sortTable('translations')"
            v-if="display.col.translations"
            :title="display.action.sort ? __('Sort by translation') : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >{{ __('Translations') }}
          </th>
          <th
            @click="sortTable('frequency', 'desc')"
            v-if="display.col.frequency"
            :title="display.action.sort ? __('Sort by word frequency') : undefined"
            :class="{ 'no-sort': !display.action.sort }"
          >{{ __('Frequency') }}
          </th>
          <th
            @click="sortTable('status')"
            v-if="display.col.status"
            :title="__('Sort by status')"
          >{{ __('Status') }}
          </th>
          <th
            @click="sortTable('lastViewed', 'desc')"
            v-if="display.col.lastSeen"
            :title="__('Sort by last seen')"
          >{{ __('Last seen') }}
          </th>
          <th v-if="display.col.actions" class="no-sort">{{ __('Actions') }}</th>
        </tr>
      </thead>
      <tbody>
        <Row v-for="(word) in usedWords" :key="word.id" :word="word" :isHighlighed="isWordHighlighted[word.original]" :display="props.display" :dictionary="props.dictionary" :profile="profile" />
      </tbody>
    </table>
  </div>
</template>


<style scoped lang="scss">
@import "@/style/global.scss";

.add-word-section {
  margin-bottom: 20px;
}

.word-table {
  width: 100%;
  border-collapse: collapse;
}

th {
  border: 1px solid $border-color;
  padding: 10px;
  text-align: left;
}

th {
  cursor: pointer;
  background-color: $table-header-color;
}

th:hover {
  background-color: $table-header-hover-color;
}

th.no-sort {
  cursor: default;
}
th.no-sort:hover {
  background-color: $table-hover-color;
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
