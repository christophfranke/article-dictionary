<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import type { Word, User } from '@/types';
import type { DictionaryCollection } from '@/dictionary/collection';
import useEdit from './use-edit';

const props = defineProps({
	word: {
		type: Object as unknown as () => Word,
		required: true,
	},
	highlightedWord: {
		type: String,
		default: '',
	},
	display: {
		type: Object,
		default: {
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
		},
	},
	dictionary: {
		type: Object as unknown as () => DictionaryCollection,
		required: true,
	},
	profile: {
		type: Object as unknown as () => User,
		required: true,
	},
});

const {
  editingTranslationId,
  editTranslationsValue,
  editTranslations,
  cancelEditTranslations,
  updateTranslation
} = useEdit(props);

const dictionaryLink = (word: Word): string => `https://glosbe.com/${props.profile.sourceLanguage}/${props.profile.targetLanguage}/${word.original}`

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


const updateWord = props.dictionary.updateWord;
const retranslateWord = props.dictionary.retranslateWord;
</script>

<template>
  <tr
  	:class="{ highlighted: word.original === highlightedWord }"
  	:id="`word-${word.id}`"
  	>
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
        <form @submit.prevent="updateTranslation" class="edit-form">
          <input type="submit" style="display: none;" />
          <button @click.prevent="cancelEditTranslations(word.id)" class="cancel-button">
            <FontAwesomeIcon icon="times" />
          </button>
          <input
            id="edit-translations"
            v-model="editTranslationsValue"
            @blur="cancelEditTranslations(word.id)"
          />
          <button @mousedown="updateTranslation">
            <FontAwesomeIcon icon="check" />
          </button>
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
</template>

<style scoped>
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
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