<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted, onBeforeUnmount } from 'vue';
import type { PropType } from 'vue';
import type { ArticleBase, ArticleDetail, Token } from '@/types';
import type { DictionaryView } from '@/dictionary/view';
import { useArticleView } from '@/use/articles';

import __ from '@/i18n'


const props = defineProps({
	dictionary: {
		type: Object as PropType<DictionaryView>,
		required: true,
	},
	highlighted: {
		type: Object as PropType<{ token: Token | null, index: number }>,
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

const inflectable = (x: string) => ['VERB', 'AUX'].includes(x)
const declinable = (x: string) => ['NOUN', 'ADJ', 'PROPN', 'NUM', 'PERSON', 'GPE', 'PRODUCT', 'EVENT', 'LOC', 'PRON', 'ORG', 'DET', 'X'].includes(x)

const posTable = {
  VERB: 'Verb',
  NOUN: 'Noun',
  ADJ: 'Adjective',
  ADV: 'Adverb',
  PROPN: 'Proper Noun',
  NUM: 'Number',
  PERSON: 'Person',
  GPE: 'Location', // political location, country, city, etc
  PRODUCT: 'Object', // food, etc
  EVENT: 'Event', // battle, etc
  LOC: 'Location', // geograical location, mountain range, water, etc
  PRON: 'Pronoun',
  ADP: 'Adposition',
  ORG: 'Organisation, Institution, etc.',
  DET: 'Determiner',
  CCONJ: 'Coordinating Conjunction',
  SCONJ: 'Subordinating Conjunction',
  PART: 'Particle',
  PUNCT: 'Punctuation',
  AUX: 'Auxiliary Verb',
  X: 'Other',
}
const genderTable = {
  'Neut': 'Neutrum',
  'Fem': 'Feminine',
  'Masc': 'Masculine',
}
const caseTable = {
  'Nom': 'Nominative',
  'Gen': 'Genitive',
  'Dat': 'Dative',
  'Acc': 'Accusative',
}
const numberTable = {
  'Sing': 'Singular',
  'Plur': 'Plural',
}
const personTable = {
  '1': 'First Person',
  '2': 'Second Person',
  '3': 'Third Person'
}
const voiceTable = {
  'Pass': 'Passive',
  'Act': 'Active',
}
const tenseTable = {
  'Past': 'Past',
  'Pres': 'Present',
  'Fut': 'Future',
}
const explain = (mark: string, table: Record<string, string>): string => {
  if (mark in table) {
    return table[mark]
  }

  return mark
}

const showStatus = computed<string[]>(() => ['new', 'seen', 'known'].filter(status => props.display[status]));
const isVisible = computed(() => !!props.highlighted.token?.word
    && showStatus.value.includes(props.dictionary.find(props.highlighted.token?.word || '')?.status || '')
);

const info = (token: Token): string[] => {
  let result = []

  if (token.pos) {
    result.push(explain(token.pos, posTable))
  }

  if (token.morph && token.pos) {
    // console.log(token.display, token.word, token.morph)
    let reflection = ''
    if (token.morph.Case && declinable(token.pos)) {
      reflection = explain(token.morph.Case, caseTable)
    }

    if (token.morph.Person && inflectable(token.pos)) {
      reflection += ' ' + explain(token.morph.Person, personTable)
    }

    if (token.morph.Number) {
      reflection += ' ' + explain(token.morph.Number, numberTable)
    }

    if (reflection) {
      result.push(reflection)
    }

    if (token.morph.Gender && declinable(token.pos)) {
      result.push(explain(token.morph.Gender, genderTable))
    }

    if (token.morph.Voice && token.morph.Voice !== 'Act' && inflectable(token.pos)) {
      result.push(explain(token.morph.Voice, voiceTable))
    }

    if (token.morph.Tense && inflectable(token.pos)) {
      result.push(explain(token.morph.Tense, tenseTable))
    }
  }

  if (token.lemma && token.lemma !== token.word) {
    result.push(token.lemma)
  }

  return result
}

const content = computed(() => {
  if (isVisible.value) {
    const token = props.highlighted.token
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
      return { text: '...', info: [__('translating')] }
    }

    return {
      text: word.translations.join(', ') || '',
      info: info(token)
    }
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
const UPDATE_TIME = 400
let original: string | undefined
let timeoutId: ReturnType<typeof setTimeout> | null = null
watch(isVisible, async (newValue, oldValue) => {
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
  if (!oldValue && newValue) {
    original = props.highlighted.token?.word;
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
		{{ content.text }}<span v-for="info in content.info"> | <i class="italic">{{ info }}</i></span>
  </div>	
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

.tooltip {
  position: fixed;
  margin: 0 50px 50px 0;
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