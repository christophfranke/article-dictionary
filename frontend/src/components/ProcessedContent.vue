<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { PropType } from 'vue';
import type { DictionaryView } from '../dictionary/view';
import type { Token, Highlight } from '@/types';

const props = defineProps({
	content: {
		type: String,
		default: '',
	},
	tokens: {
		type: Array as PropType<Token[]>,
		required: true,
	},
	dictionary: {
		type: Object as PropType<DictionaryView | null>,
		default: null
	},
	modelValue: {
    type: Object as PropType<Highlight>,
		default: {
      token: null,
      index: null,
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


type ProcessedContentItem = {
  token: Token;
  separator: string[];
}

const createEmptyToken = () => ({
  display: '',
  word: '',
  space: '',
  ignore: true,
})

const sanitizedContent = computed<string>(() => props.content || props.tokens.map(token => token.display).join(', '))

const getSeparator = (index: number, nextWord: string): string => {
  const nextIndex = sanitizedContent.value.substring(index).indexOf(nextWord);
  return nextIndex === -1 || nextIndex === 0
    ? ''
    : sanitizedContent.value.substring(index, index + nextIndex);
};

const processedContent = computed<ProcessedContentItem[]>(() => {
  const result: ProcessedContentItem[] = [];
  let currentIndex = 0;

  props.tokens.forEach((token, index) => {
    const separator = getSeparator(currentIndex, token.display);
    result.push({
      token,
      separator: separator.split('\n')
    });

    currentIndex += separator.length + token.display.length;
  });

  if (currentIndex < sanitizedContent.value.length) {
    const separator = sanitizedContent.value.substring(currentIndex).split('\n');
    result.push({ token: createEmptyToken(), separator });
  }

  return result;
});


let internalHighlightedWord = ''
const setHighlight = (update: Highlight) => {
  if (update.token) {
  	internalHighlightedWord = update.token.word;
    emit('update:modelValue', update);
  }
};
const unsetHighlight = (update: Highlight) => {
	if (internalHighlightedWord === update.token?.word) {
		internalHighlightedWord = '';
		emit('update:modelValue', { word: '', index: -1 });
  }
};

const isNewWord = (word: string): boolean => {
  return props.dictionary?.find(word)?.status === 'new'
}
const isSeenWord = (word: string): boolean => {
  return props.dictionary?.find(word)?.status === 'seen'
}

const unique = `${Math.random()}`.substring(2, 6);
onMounted(() => {
  if (props.scrollToIndex) {
    const word = document.getElementById(`word-${unique}-${props.scrollToIndex}`);
    if (word) {
      word.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
})
</script>

<template>
  <template v-for="({ token, separator }, index) in processedContent" :key="index">
    <span class="separator">
      <template v-for="(sep, sepIndex) in separator">
        {{ sep }}<br v-if="sepIndex < separator.length - 1" />
      </template>
    </span>
    <span
      @mouseover="setHighlight({ token, index })"
      @mouseout="unsetHighlight({ token, index })"
      @click="event => emit('click', { token, index }, event)"
      :id="`word-${unique}-${index}`"
      :class="{
        padding: props.display.padding,
        clickable: props.display.click,
        new: props.display.highlight.new && isNewWord(token.word),
        seen: props.display.highlight.seen && isSeenWord(token.word),
        mark: props.display.highlight.mark && token.word === mark,
      }"
    >
      {{ token.display }}
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