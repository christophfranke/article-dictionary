<script setup lang="ts">
import { ref, computed } from 'vue';
import createDictionaryCollection from '../dictionary/collection';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import type { Word } from '../types/index.ts';


const props = defineProps({
  dictionary: {
    type: Object as unknown as () => ReturnType<typeof createDictionaryCollection>,
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
      }
    }
  }
});

const dict = props.dictionary;
const words = computed<Word[]>(() => dict.get());

const newWord = ref<string>('');
const editingTranslationId = ref<string>('');
const editTranslationsValue = ref<string>('');
const editTranslationsInput = ref<HTMLInputElement[] | null>(null);

const sortOrder = ref<string>('asc');
const sortedBy = ref<string>(props.sort);

const sortTable = (column: string): void => {
  if (!props.display.action.sort) {
    return
  }

  if (column === sortedBy.value) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortedBy.value = column;
    sortOrder.value = 'asc';
  }
};

const sortedWords = computed<Array<Word>>(() => {
  const sorted = [...words.value];
  if (sortedBy.value) {
    sorted.sort((a, b) => {
      const order = sortOrder.value === 'asc' ? 1 : -1;

      // Access property values
      const propertyA = (a as any)[sortedBy.value];
      const propertyB = (b as any)[sortedBy.value];

      // Use localeCompare for string comparison with locale awareness
      if (typeof propertyA === 'string' && typeof propertyB === 'string') {
        return propertyA.localeCompare(propertyB) * order;
      }

      // For non-string properties, use regular comparison
      return propertyA > propertyB ? order : -order;
    });
  }

  if (props.display.limit > 0) {
    return sorted.slice(0, props.display.limit);
  }

  return sorted;
});

const editTranslations = async (id: string): Promise<void> => {
  if (props.display.action.edit) {
    editingTranslationId.value = id;
    if (id) {
      const word: Word | undefined = words.value.find((word) => word.id === id);

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

const stopEditTranslations = async (id: string): Promise<void> => {
  await new Promise(resolve => setTimeout(resolve, 0));

  if (editingTranslationId.value === id) {
    editingTranslationId.value = '';
  }
};



const isUpdating = ref(false)
const updateTranslation = async (e: Event): Promise<void> => {
  e.preventDefault();
  if (isUpdating.value) {
    return
  }

  isUpdating.value = true;
  const word: Word | undefined = words.value.find((word) => word.id === editingTranslationId.value);

  if (word) {
    const translations: string[] = editTranslationsValue.value.split(',').map((t) => t.trim());
    await updateWord(word.original, { translations });
    editingTranslationId.value = '';
  }

  isUpdating.value = false;
};

const setStatus = async (word: Word, status: string): Promise<void> => {
  await updateWord(word.original, { status });
};

const changeStatus = async (word: Word): Promise<void> => {
  if (!props.display.action.status) {
    return
  }

  const statusOptions: string[] = ['new', 'seen', 'known', 'ignore'];
  const currentIndex: number = statusOptions.indexOf(word.status);
  const newIndex: number = (currentIndex + 1) % statusOptions.length;
  const newStatus: string = statusOptions[newIndex];

  await updateWord(word.original, { status: newStatus });
};

const addWord = async (): Promise<void> => {
  if (newWord.value) {
    await dict.addWord(newWord.value);
    newWord.value = '';
  }
};

const updateWord = dict.updateWord;
const retranslateWord = dict.retranslateWord;
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
          <th @click="sortTable('number')" v-if="display.col.number">#</th>
          <th @click="sortTable('original')" v-if="display.col.original">Original</th>
          <th @click="sortTable('translations')" v-if="display.col.translations">Translations</th>
          <th @click="sortTable('status')" v-if="display.col.status">Status</th>
          <th v-if="display.col.actions">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(word) in sortedWords" :key="word.id" :class="{ highlighted: word.original === highlight.toLowerCase() }">
          <td v-if="display.col.number">{{ word.index }}</td>
          <td v-if="display.col.original">{{ word.original }}</td>
          <template v-if="display.col.translations">
            <td @mousedown="editTranslations(word.id)" v-if="word.id !== editingTranslationId">
              {{ word.translations.join(', ') }}
            </td>
            <td v-else>
              <form @submit="updateTranslation" class="edit-form">
                <button @click="stopEditTranslations(word.id)">x</button>
                <input
                  ref="editTranslationsInput"
                  v-model="editTranslationsValue"
                  @blur="stopEditTranslations(word.id)"
                />
                <button @mousedown="updateTranslation">ok</button>
              </form>
            </td>
          </template>
          <td v-if="display.col.status" @click="changeStatus(word)" class="status-column">{{ word.status }}</td>
          <td v-if="display.col.actions" class="actions-column">
            <div>
              <button v-if="display.action.known" @click="setStatus(word, 'known')"><FontAwesomeIcon icon="check-circle" /></button>
              <button v-if="display.action.ignore" @click="setStatus(word, 'ignore')"><FontAwesomeIcon icon="times-circle" /></button>
              <button v-if="display.action.retranslate" @click="retranslateWord(word.original)"><FontAwesomeIcon icon="rotate-left" /></button>
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

.highlighted {
  background-color: rgba(255, 191, 128, 0.25);
}


.status-column {
  cursor: pointer;
}

.status-column:hover {
  background-color: #f9f9f9;
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
