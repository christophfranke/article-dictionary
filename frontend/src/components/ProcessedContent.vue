<script setup lang="ts">
import { ref, computed } from 'vue';
import type { DictionaryView } from '../dictionary/view';

const { content, words, dictionary } = defineProps({
	content: {
		type: String,
		default: '',
	},
	words: {
		type: Array as unknown as () => string[],
		required: true,
	},
	dictionary: {
		type: Object as unknown as () => DictionaryView | null,
		default: null
	},
	modelValue: {
		type: String,
		default: '',
	},
  mark: {
    type: String,
    default: '',
  },
  display: {
    default: {
      padding: true,
      click: true,
      highlight: {
        new: true,
        seen: true,
        mark: true,
      }
    }
  }
});

const emit = defineEmits(['update:modelValue', 'click']);


interface ProcessedContentItem {
  word: string;
  separator: string[];
}

const sanitizedContent = computed<string>(() => content || words.join(', '))

const getSeparator = (index: number, nextWord: string): string => {
  const nextIndex = sanitizedContent.value.substring(index).indexOf(nextWord);
  return nextIndex === -1 || nextIndex === 0
    ? ''
    : sanitizedContent.value.substring(index, index + nextIndex);
};

const processedContent = computed<ProcessedContentItem[]>(() => {
  const result: ProcessedContentItem[] = [];
  let currentIndex = 0;

  words.forEach((word, index) => {
    const separator = getSeparator(currentIndex, word);
    result.push({ word, separator: separator.split('\n') });
    currentIndex += separator.length + word.length;
  });

  if (currentIndex < sanitizedContent.value.length) {
    const separator = sanitizedContent.value.substring(currentIndex).split('\n');
    result.push({ word: '', separator });
  }

  return result;
});


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
  <template v-for="({ word, separator }, index) in processedContent" :key="index">
    <span class="separator">
      <template v-for="(sep, index) in separator">
        {{ sep }}<br v-if="index < separator.length - 1" />
      </template>
    </span>
    <span
      @mouseover="setHighlight(word)"
      @mouseout="unsetHighlight(word)"
      @click="event => emit('click', word, event)"
      :class="{
        padding: display.padding,
        clickable: display.click,
        new: display.highlight.new && dictionary?.find(word)?.status === 'new',
        seen: display.highlight.seen && dictionary?.find(word)?.status === 'seen',
        mark: display.highlight.mark && word === mark,
      }"
    >
      {{ word }}
    </span>
  </template>
</template>

<style scoped>
span.padding {
  padding: 2px 3px;
}

span.clickable {
  cursor: pointer;
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

span.mark {
  background-color: rgba(204, 22, 22, 0.5);
}
</style>	