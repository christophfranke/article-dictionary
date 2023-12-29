<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue';

import type { PropType } from 'vue';
import type { Word, Profile } from '@/types';
import type { DictionaryView } from '@/dictionary/view';

import useEdit from './use-edit';
import useTime from '@/use/time';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Button from '@/elements/Button.vue';
import ButtonLink from '@/elements/ButtonLink.vue';
import Input from '@/elements/Input.vue';


const props = defineProps({
	word: {
		type: Object as PropType<Word>,
		required: true,
	},
	isHighlighed: {
		type: Boolean,
		default: false,
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
				glosbe: true,
        detail: true,
        link: true,
			},
		},
	},
	dictionary: {
		type: Object as PropType<DictionaryView>,
		required: true,
	},
	profile: {
		type: Object as PropType<Profile>,
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

const dictionaryLink = (word: Word): string => `https://glosbe.com/${props.profile.sourceLanguage}/${props.profile.targetLanguage}/${word.original}`;

const routerLink = (word: Word): string => `/dictionary/${word.original}`;

const setStatus = async (word: Word, status: string): Promise<void> => {
  await updateWord(word.id, { status });
};

const { timeAgo } = useTime();

const lastSeen = computed(() => {
  if (!props.display.col.lastSeen) {
    return
  }

  if (!props.word.lastViewed) {
    return ''
  }

  return timeAgo(props.word.lastViewed);
});


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

  await updateWord(word.id, { status: nextStatus(word.status) });
};


const updateWord = props.dictionary.updateOne;
const retranslateWord = props.dictionary.retranslate;
</script>

<template>
  <tr
  	:class="{ highlighted: isHighlighed }"
  	:id="`word-${word.id}`"
  	>
    <td v-if="display.col.number">{{ word.order + 1 }}</td>
    <td v-if="display.col.original" :class="{ 'original-td-link': display.action.link }">
      <RouterLink
        v-if="display.action.link"
        :to="routerLink(word)"
        title="Inspect word"
        class="original-link"
      >
        {{ word.original }}
      </RouterLink>
      <span v-else>{{ word.original }}</span>
    </td>
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
          <Button @click.prevent="cancelEditTranslations(word.id)" role="view">
            <FontAwesomeIcon icon="times" />
          </Button>
          <Input
            id="edit-translations"
            v-model="editTranslationsValue"
            @blur="cancelEditTranslations(word.id)"
          />
          <Button @mousedown="updateTranslation">
            <FontAwesomeIcon icon="check" />
          </Button>
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
    <td v-if="display.col.lastSeen">{{ lastSeen }}</td>
    <td v-if="display.col.actions" class="actions-column">
      <div>
        <Button
          v-if="display.action.known"
          @click="setStatus(word, 'known')"
          title="Mark as known"
          size="small"
        >
          <FontAwesomeIcon icon="check-circle" />
        </Button>
        <Button
          v-if="display.action.ignore"
          @click="setStatus(word, 'ignore')"
          title="Ignore word"
          size="small"
        >
          <FontAwesomeIcon icon="ban" />
        </Button>
        <Button
          v-if="display.action.retranslate"
          @click="retranslateWord(word.id)"
          title="Retranslate word"
          size="small"
        >
          <FontAwesomeIcon icon="rotate-left" />
        </Button>
        <ButtonLink
          v-if="display.action.detail"
          :to="routerLink(word)"
          title="Inspect word"
          size="small"
          class="inspect-word-action"
        >
          <FontAwesomeIcon icon="eye" />
        </ButtonLink>
        <a
          v-if="display.action.glosbe"
          :href="dictionaryLink(word)"
          target="_blank"
          title="Open Glosbe Dictionary"
        >
          <Button role="view" size="small"><FontAwesomeIcon icon="globe" /></Button>
        </a>
      </div>
    </td>
  </tr>	
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

td {
  border: 1px solid $border-color;
  padding: 10px;
  text-align: left;
}

.highlighted {
  background-color: $table-highlight-color;
}

.original-td-link {
  padding: 0;

  &:hover {
    background-color: $table-hover-color;  
  }
}

.original-link {
  padding: 10px;
  display: block;
  width: 100%;
  height: 100%;
}

.original-link {
  &, &:visited {
    color: inherit;
  }
}


.status-column {
  cursor: pointer;

  &:hover {
    background-color: $table-hover-color;
  }
}

.edit-column {
  cursor: pointer;
  
  &:hover {
    background-color: $table-hover-color;
  }
}

.edit-form {
  display: flex;
  align-items: center;

  button {    
    padding: 5px 10px;
    margin-right: 5px;
    margin-left: 5px;
  }

  input {
    flex: 1;
    padding: 2px 5px;
  }
}

.actions-column div {
  display: flex;
  justify-content: space-around;
  align-items: stretch;
}

.actions-column {
  button, .inspect-word-action {
    margin: 0 2px;
  }
}

</style>