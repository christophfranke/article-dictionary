<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue';
import type { DictionaryCollection } from '@/dictionary/collection';
import { useProfile } from '@/use/user';
import useScroll from './dictionary-table/use-scroll';
import useSort from './dictionary-table/use-sort';
import useEdit from './dictionary-table/use-edit';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import type { Word } from '../types/index.ts';


const props = defineProps({
  dictionary: {
    type: Object as unknown as () => DictionaryCollection,
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
        link: true,
      },
      behaviour: {
        highlight: true,
        scroll: true,
      }
    }
  }
});


const { rows } = useScroll(props);
const { sortTable, sortedWords } = useSort(props);
const {
  editingTranslationId,
  editTranslationsValue,
  editTranslationsInput,
  editTranslations,
  stopEditTranslations,
  updateTranslation
} = useEdit(props)

const profile = useProfile();
const dictionaryLink = (word: Word): string => `https://glosbe.com/${profile.sourceLanguage.value}/${profile.targetLanguage.value}/${word.original}`

const setStatus = async (word: Word, status: string): Promise<void> => {
  await updateWord(word.original, { status });
};


const statusOptions: string[] = ['new', 'seen', 'known'];
const nextStatus = (status: string): string => {
  const currentIndex: number = statusOptions.indexOf(status);
  const newIndex: number = (currentIndex + 1) % statusOptions.length;
  return statusOptions[newIndex];
};

const changeStatus = async (word: Word): Promise<void> => {
  if (!props.display.action.status) {
    return
  }

  await updateWord(word.original, { status: nextStatus(word.status) });
};


const newWord = ref<string>('');
const addWord = async (): Promise<void> => {
  if (newWord.value) {
    await props.dictionary.addWord(newWord.value);
    newWord.value = '';
  }
};

const updateWord = props.dictionary.updateWord;
const retranslateWord = props.dictionary.retranslateWord;
</script>

<template>
  <div class="dictionary-table">
    <div v-if="display.action.add" class="add-word-section">
      <label for="newWord">New Entry:</label>
      <input v-model="newWord" id="newWord" />
      <button @click="addWord">Add</button>
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
            @click="sortTable('frequency')"
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
        <tr v-for="(word) in sortedWords" :key="word.id" :class="{ highlighted: display.behaviour.highlight && word.original === highlight.toLowerCase() }" ref="rows" :id="`word-${word.id}`">
          <td v-if="display.col.number">{{ word.index + 1 }}</td>
          <td v-if="display.col.original">{{ word.original }}</td>
          <template v-if="display.col.translations">
            <td
              @mousedown="editTranslations(word.id)"
              v-if="word.id !== editingTranslationId"
              :class="{ 'edit-column': display.action.edit }"
              :title="display.action.edit ? 'Edit translations' : undefined"
            >{{ word.translations.join(', ') }}
            </td>
            <td v-else>
              <form @submit="updateTranslation" class="edit-form">
                <button @click="stopEditTranslations(word.id)" class="cancel-button">x</button>
                <input
                  ref="editTranslationsInput"
                  v-model="editTranslationsValue"
                  @blur="stopEditTranslations(word.id)"
                />
                <button @mousedown="updateTranslation">ok</button>
              </form>
            </td>
          </template>
          <td v-if="display.col.frequency">{{ word.frequency }}</td>
          <td
            v-if="display.col.status"
            @click="changeStatus(word)"
            :title="display.action.status ? `Change status to ${nextStatus(word.status)}` : undefined"
            :class="{ 'status-column': display.action.status }"
          >{{ word.status }}
          </td>
          <td v-if="display.col.actions" class="actions-column">
            <div>
              <button
                v-if="display.action.known"
                @click="setStatus(word, 'known')"
                title="Mark as known"
              >
                <FontAwesomeIcon icon="check-circle" />
              </button>
              <button
                v-if="display.action.ignore"
                @click="setStatus(word, 'ignore')"
                title="Ignore word"
              >
                <FontAwesomeIcon icon="ban" />
              </button>
              <button
                v-if="display.action.retranslate"
                @click="retranslateWord(word.original)"
                title="Retranslate word"
              >
                <FontAwesomeIcon icon="rotate-left" />
              </button>
              <a
                v-if="display.action.link"
                :href="dictionaryLink(word)"
                target="_blank"
                title="Open Glosbe Dictionary"
              >
                <button><FontAwesomeIcon icon="globe" /></button>
              </a>
            </div>
          </td>
        </tr>
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

th, td {
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

.highlighted {
  background-color: rgba(255, 191, 128, 0.25);
}


.status-column {
  cursor: pointer;
}

.status-column:hover {
  background-color: #f9f9f9;
}

.edit-column {
  cursor: pointer;
}

.edit-column:hover {
  background-color: #f9f9f9;
}

.edit-form {
  display: flex;
  align-items: center;
}

.edit-form button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
  transition: background-color 0.3s ease;
}


.edit-form button:hover {
  background-color: #0056b3;
}

.edit-form button.cancel-button {
  background-color: #b0c4de;
}
.edit-form button.cancel-button:hover {
  background-color: #a9a9a9;
}

.edit-form input {
  flex: 1;
  padding: 2px 5px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
/*  outline: none;*/
}


.actions-column div {
  display: flex;
  justify-content: center;
  align-items: stretch;
}

.actions-column button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
  transition: background-color 0.3s ease;
}

.actions-column button:hover {
  background-color: #0056b3;
}

.edit-form {
  display: flex;
  align-items: center;
}

.edit-form input {
  margin-right: 5px;
}
</style>
