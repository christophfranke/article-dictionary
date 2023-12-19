<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { PropType } from 'vue';
import type { DictionaryView } from '../dictionary/view';

type ModelType = {
  word: string;
  index: number;
}

const { content, words, dictionary, mark, scrollToIndex } = defineProps({
	content: {
		type: String,
		default: '',
	},
	words: {
		type: Array as PropType<string[]>,
		required: true,
	},
	dictionary: {
		type: Object as PropType<DictionaryView | null>,
		default: null
	},
	modelValue: {
    type: Object as PropType<ModelType>,
		default: {
      word: null,
      index: null
    },
	},
  mark: {
    type: String,
    default: '',
  },
  scrollToIndex: {
    type: Number,
    default: -1,
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
const setHighlight = (update: ModelType) => {
  if (update.word) {    
  	internalHighlightedWord = update.word;
    emit('update:modelValue', update);
  }
};
const unsetHighlight = (update: ModelType) => {
	if (internalHighlightedWord === update.word) {
		internalHighlightedWord = '';
		emit('update:modelValue', { word: '', index: -1 });
  }
};

const unique = `${Math.random()}`.substring(2, 6);

onMounted(() => {
  if (scrollToIndex) {
    const word = document.getElementById(`word-${unique}-${scrollToIndex}`);
    if (word) {
      word.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
})
</script>

<template>
  <template v-for="({ word, separator }, index) in processedContent" :key="index">
    <span class="separator">
      <template v-for="(sep, sepIndex) in separator">
        {{ sep }}<br v-if="sepIndex < separator.length - 1" />
      </template>
    </span>
    <span
      @mouseover="setHighlight({ word, index })"
      @mouseout="unsetHighlight({ word, index })"
      @click="event => emit('click', { word, index }, event)"
      :id="`word-${unique}-${index}`"
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

<style scoped lang="scss">
@import "@/style/global.scss";

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
  background-color: $content-new-word-color;
}

span.seen {
  background-color: $content-seen-word-color;
}

span.mark {
  background-color: $content-mark-word-color;
}
</style>	