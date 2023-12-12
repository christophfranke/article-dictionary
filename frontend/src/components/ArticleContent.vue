<script setup lang="ts">
import { ref, computed } from 'vue';
import type { DictionaryCollection } from '../dictionary/collection';

const { content, words, dictionary } = defineProps({
	content: {
		type: String,
		required: true,
	},
	words: {
		type: Array as unknown as () => string[],
		required: true,
	},
	dictionary: {
		type: Object as unknown as () => DictionaryCollection,
		required: true,
	},
	modelValue: {
		type: String,
		default: '',
	},
});

const emit = defineEmits(['update:modelValue']);


interface ProcessedContentItem {
  word: string;
  separator: string[];
}


const getSeparator = (index: number, nextWord: string): string => {
  const nextIndex = content.substring(index).indexOf(nextWord);
  return nextIndex === -1 || nextIndex === 0
    ? ''
    : content.substring(index, index + nextIndex);
};

const processedContent = computed<ProcessedContentItem[]>(() => {
  const result: ProcessedContentItem[] = [];
  let currentIndex = 0;

  words.forEach((word, index) => {
    const separator = getSeparator(currentIndex, word);
    result.push({ word, separator: separator.split('\n') });
    currentIndex += separator.length + word.length;
  });

  return result;
});

const toggleStatusSeen = (word: string) => {
  const original = word.toLowerCase()
  dictionary.updateWord(original, { status: ['new', 'seen'].includes(dictionary.find(original)?.status || '') ? 'known' : 'seen' });
};


let internalHighlightedWord = ''
const setHighlight = (word: string) => {
	internalHighlightedWord = word;
  emit('update:modelValue', word);
};
const unsetHighlight = (word: string) => {
	if (internalHighlightedWord === word) {
		internalHighlightedWord = '';
		emit('update:modelValue', '');
  }
};

</script>

<template>
  <p>
    <template v-for="({ word, separator }, index) in processedContent" :key="index">
      <span class="separator">
        <template v-for="(sep, index) in separator">
          {{ sep }}<br v-if="index < separator.length - 1" />
        </template>
      </span>
      <span
        @mouseover="setHighlight(word)"
        @mouseout="unsetHighlight(word)"
        @click="toggleStatusSeen(word)"
        :class="{ word: true, new: dictionary.find(word.toLowerCase())?.status === 'new', seen: dictionary.find(word.toLowerCase())?.status === 'seen' }"
      >
        {{ word }}
      </span>
    </template>
  </p>
</template>

<style scoped>
p {
  font-size: 18px;
  line-height: 2;
}

span.word {
  cursor: pointer;
  padding: 2px 3px;
}

span.separator {
  padding: 2px 0;
  margin: 0 -2px;
}

span.new {
  background-color: rgba(51, 153, 255, 0.15);
}

span.seen {
  background-color: rgba(255, 191, 128, 0.25);
}
</style>	