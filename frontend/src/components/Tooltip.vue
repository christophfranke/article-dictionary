<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted, onBeforeUnmount } from 'vue';
import type { PropType } from 'vue';
import type { ArticleBase, ArticleDetail } from '@/types';
import type { DictionaryView } from '@/dictionary/view';
import { useArticleView } from '@/use/articles';

import __ from '@/i18n'


const props = defineProps({
	dictionary: {
		type: Object as PropType<DictionaryView>,
		required: true,
	},
	highlighted: {
		type: Object as PropType<{ word: string, index: number }>,
		required: true
	},
  article: {
    type: Object as PropType<ArticleDetail>,
    default: null,
  },
  display: {
    type: Object,
    default: {
      new: true,
      seen: true,
      known: false,
      update: {
        seen: true
      }
    }
  }
});

const explanationTable = {
  VERB: 'Verb',
  NOUN: 'Noun',
  ADJ: 'Adjective',
  ADV: 'Adverb',
  PROPN: 'Proper Noun',
  NUM: 'Number',
  PERSON: 'Person',
  GPE: 'Country, City, State',
  PRODUCT: 'Object, Vehicle, Food, etc.',
  PRON: 'Pronoun',
  ADP: 'Adposition',
  ORG: 'Organisation, Institution, etc.',
  DET: 'Determiner',
  CCONJ: 'Coordinating Conjunction',
  SCONJ: 'Subordinating Conjunction',
  PART: 'Particle',
  X: 'Other',
}
const explain = (mark: string): string => {
  // @ts-ignore
  return explanationTable[mark] ?? mark
}

const showStatus = computed<string[]>(() => ['new', 'seen', 'known'].filter(status => props.display[status]));
const isVisible = computed(() => !!props.highlighted.word
    && showStatus.value.includes(props.dictionary.find(props.highlighted.word || '')?.status || '')
);

const content = computed(() => {
  if (isVisible.value) {
    const token = props.article.tokens[props.highlighted.index]
    if (!token || token.ignore) {
      console.log('no token', token)
      return null
    }

    const original = token.word
    const word = props.dictionary.find(token.word)
    if (!word) {
      console.log('no word', original)
      return null
    }

    if (word.needsRetranslate) {
      return { text: '...', info: __('translating') }
    }

    return { text: word.translations.join(', ') || '', info: explain(token.pos) }
  }

  return null
});

const position = reactive({ x: 0, y: 0 });
const setTooltipPosition = (event: MouseEvent): void => {
  position.x = event.clientX + 10; // Add an offset to prevent the tooltip from overlapping with the cursor
  position.y = event.clientY + 20; // Adjust the offset based on your design preference
};

const { articles } = useArticleView();
const markArticleAsSeen = (article: ArticleBase, index: number) => {
  return articles.markSeen({ id: article.id, index });
}


// time how long a translation must be shown before it counts as seen
const UPDATE_TIME = 500
let original = ''
let timeoutId: ReturnType<typeof setTimeout> | null = null
watch(isVisible, async (newValue, oldValue) => {
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
  if (!oldValue && newValue) {
    original = props.highlighted.word;
    const word = props.dictionary.find(original)
    if (word?.needsRetranslate) {
      await props.dictionary.getWord(word.id)
    }

    timeoutId = setTimeout(() => {
      if (props.display.update.seen) {
        const word = props.dictionary.find(original)
        if (word) {
          props.dictionary.markSeen(word.id);
        }
        if (props.article && props.article.status !== 'read') {
          markArticleAsSeen(props.article, props.highlighted.index);
        }
      }
    }, UPDATE_TIME);
  }
  if (!newValue && oldValue) {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  }
});



onMounted(() => {
  document.addEventListener('mousemove', setTooltipPosition);
});

onBeforeUnmount(() => {
  document.removeEventListener('mousemove', setTooltipPosition);
});
</script>

<template>
  <div v-if="isVisible && !!content" class="tooltip" :style="{ top: `${position.y}px`, left: `${position.x}px` }">
		<span>{{ content.text }} | <i class="italic">{{ content.info }}</i></span>
  </div>	
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

.tooltip {
  position: fixed;
  z-index: 10;
  background-color: $tooltip-background-color;
  color: $tooltip-color;
  padding: 5px;
  border-radius: 5px;
  font-size: ($tooltip-font-size);
  pointer-events: none; /* Ensures tooltip doesn't interfere with mouse events */
}
.italic {
  // font-size: ($tooltip-font-size - 2px);
}
</style>