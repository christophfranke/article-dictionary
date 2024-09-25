<script setup lang="ts">
import { ref, computed, watch, watchEffect, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import type { WordDetail, PartialWord, ArticleDetail, Highlight } from '@/types';
import { useDictionaryView } from '@/use/dictionary';
import { useArticleView } from '@/use/articles';
import useReview from '@/use/review';
import type { ScoreFunction, ScoreMap } from '@/use/review';

import ProcessedContent from '@/components/ProcessedContent.vue';
import Tooltip from '@/components/Tooltip.vue';

import Headline from '@/elements/Headline.vue';
import Paragraph from '@/elements/Paragraph.vue';
import Button from '@/elements/Button.vue';

import __ from '@/i18n'


const contentDisplay = {
    padding: true,
    click: false,
    highlight: {
        new: false,
        seen: false,
        mark: true,
        underline: false,
    }	
};

const tooltipDisplay = {
    new: true,
    seen: true,
    known: true,
    update: {
        seen: false
    }	
}

const route = useRoute();
const name = route.name;
const slug = route.params.slug as string;

const { articles } = useArticleView();
const article = computed<ArticleDetail | null | undefined>(() => slug ? articles.detail(slug).value : null);

const generalScoreFn = (scores: ScoreMap): number => scores.due * scores.importance + 0.2 * Math.random()
const generalFilterFn = (word: PartialWord): boolean => !recentlyShown.includes(word.id)
    && ['seen', 'known'].includes(word.status)

// bias towards words that are close to the readingIndex of the article
const wordIndexMap = computed(() => article.value?.tokens.reduce((acc, token, index) => {
    const word = token.word
    if (!acc[word]) {
        acc[word] = [index]
    } else {
        acc[word].push(index)
    }
    return acc;
}, {} as { [key: string]: number[] }) || {});

const articleScoreFn = (scores: ScoreMap, word: PartialWord): number => {
    const wordIndices = wordIndexMap.value[word.original];
    const readingIndex = article.value?.readingIndex
    const length = article.value?.tokens.length;
    if (!wordIndices || !length && (!readingIndex && readingIndex !== 0)) {
        return 0;
    }

    const bias = wordIndices.reduce(
        (max, wordIndex) =>
            Math.max(max, 1 - Math.abs(wordIndex - readingIndex!) / length!),
        0
    );
    return (1 + bias) * scores.importance;
}
const articleFilterFn = (word: PartialWord): boolean => !recentlyShown.includes(word.id)
    && ['seen', 'new'].includes(word.status)
    && !!wordIndexMap.value[word.original]

const recentlyShown: string[] = [];
const { dictionary } = useDictionaryView(name === 'word-review' ? generalFilterFn : articleFilterFn);
const { pickSentence, findWordForReview } = useReview(dictionary, name === 'word-review' ? generalScoreFn : articleScoreFn);

const wordId = ref<string | null>(null);
const word = computed<WordDetail | null>(() => {
    if (wordId.value) {		
        const original = dictionary.findById(wordId.value)?.original
        return wordId.value && original && dictionary.detail(original).value || null
    }

    return null;
});

const sentence = computed(() => {
    if (!word.value || !word.value.sentences || !word.value.sentences.length) {
        return null;
    }

    return word.value.sentences[pickSentence(word.value.sentences)] || null;
});


watch(wordId, async () => {
    if (wordId.value) {
        const newWord = dictionary.findById(wordId.value);
        if (newWord) {
            await dictionary.get(newWord.original);
        }
    }
});

const highlight = ref<Highlight>({ token: null, index: -1});
const sanitizedHighlight = computed(() => {
    return !highlight.value || highlight.value?.token?.word === word.value?.original
        ? { token: null, index: -1 }
        : highlight.value
});

const phase = ref('recall');

const RECENTLY_SHOWN_LIMIT = 15
const markRecentlyShown = (word: WordDetail) => {
    recentlyShown.push(word.id);
    if (recentlyShown.length > RECENTLY_SHOWN_LIMIT) {
        recentlyShown.shift();
    }
}

const showTranslation = () => {
    markRecentlyShown(word.value!)
    dictionary.markSeen(word.value!.id);
    phase.value = 'review';
}

type LevelFn = (x: number) => number
type TooltipFn = (x: number) => string
type Response = {
    label: string,
    fn: LevelFn,
    tooltip: TooltipFn
}
const responses: { [key: string]: Response } = {
    '1': {
        label: __('No chance'),
        tooltip: () => __('Set level back to 1'),
        fn: level => 1,
    },
    '2': {
        label: __('Almost'),
        tooltip: newLevel => __('Decrease level to $1', newLevel),
        fn: level => (level > 1 ? level - 1 : 1),
    },
    '3': {
        label: __('Keep level'),
        tooltip: newLevel => __('Keep level at $1', newLevel),
        fn: level => level,
    },
    '4': {
        label: __('Got it'),
        tooltip: newLevel => __('Increase level to $1', newLevel),
        fn: level => level + 1,
    },
    '5': {
        label: __('Too easy'),
        tooltip: newLevel => __('Increase level by 2 to $1', newLevel),
        fn: level => level + 2,
    }
};
const nextWord = () => {
    wordId.value = findWordForReview();
    phase.value = 'recall';
}
const skipWord = () => {
    markRecentlyShown(word.value!);
    nextWord();	
}
const recordResponse = async (response: string | number) => {
    let reviewLevel = word.value!.reviewLevel || 1;

    reviewLevel = responses[response]?.fn(reviewLevel) || 1;

    if (reviewLevel < 1) {
        reviewLevel = 1;
    }

    await dictionary.updateOne(word.value!.id, { reviewLevel });
    nextWord();
}

const setIgnore = async () => {
    if (word.value) {
        await dictionary.updateOne(word.value.id, { status: 'ignore' });
    }

    nextWord();
}

const handleKeyPress = (event: KeyboardEvent) => {
    if (event.key === 'ArrowRight') {
        skipWord(); // Call skipWord function when the right arrow key is pressed
    }

    if (phase.value === 'recall') {
        if (event.key === 'Enter') {
            showTranslation();
        }
    } else if (phase.value === 'review') {
        if (Object.keys(responses).includes(event.key)) {
            recordResponse(event.key); // Handle response keys
        }
    }
}

const isInitializing = ref(true);
onMounted(async () => {
    document.addEventListener('keydown', handleKeyPress);

    if (!dictionary.items.value.length) {
        await dictionary.load();
    }

    if (slug && !article.value) {
        await articles.get(slug);
    }

    if (!wordId.value) {
        wordId.value = findWordForReview();
    }

    isInitializing.value = false;
});

onUnmounted(() => {
    document.removeEventListener('keydown', handleKeyPress);
});
</script>


<template>
    <div class="container">
        <div v-if="isInitializing">
            <Headline type="h2">{{ __('Loading...') }}</Headline>
        </div>
        <div v-if="!isInitializing && !wordId">
            <Headline class="done">{{ __('No words to review!') }}</Headline>
        </div>
        <div class="flashcard" v-if="word">
            <span class="level">{{ __(word.status) }} ({{ word.reviewLevel }})</span>
            <Headline class="original" type="h2">{{ word.original }}</Headline>
            <Paragraph class="example-sentence" v-if="sentence">
                <ProcessedContent
                    :content="sentence.text"
                    :tokens="sentence.tokens"
                    :dictionary="dictionary"
                    :mark="word.original"
                    :display="contentDisplay"
                    v-model="highlight"
                    :key="word.id"
                />
            </Paragraph>
            <div v-if="phase === 'recall'">
            <!-- Recall phase content if any -->
            </div>
            <div v-else>
                <ul class="translations">
                    <li v-for="translation in word.translations" :key="translation">{{ translation }}</li>
                </ul>
                <div class="response-buttons">
                    <Button v-for="(response, key) in responses" :key="key" :title="response.tooltip(response.fn(word.reviewLevel))" @click="recordResponse(key)">
                        {{ response.label }} ({{ key }})
                    </Button>
                </div>
            </div>
            <div class="show-buttons">
                <Button :title="__('Ignore word in dictionary')" @click="setIgnore"><FontAwesomeIcon icon="ban" /></Button>
                <Button role="view" @click="showTranslation" v-if="phase === 'recall'">
                    {{ __('Show Translation') }}&nbsp;&#8629;
                </Button>
                <Button :title="__('Skip word for now')" role="view" @click="skipWord">
                    {{ __('Skip') }}&nbsp;&#8594;
                </Button>
            </div>
        </div>
        <Tooltip :highlighted="sanitizedHighlight" :dictionary="dictionary" :display="tooltipDisplay" />
    </div>
</template>



<style scoped lang="scss">
@import '@/style/global.scss';

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 100px;
}


.flashcard {
	position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border: 1px solid $border-color;
  border-radius: 10px;
  margin: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.flashcard > div {
  width: 100%;
}

.level {
	position: absolute;
	top: 10px;
	right: 10px;
	font-size: 14px;
}

.original {
	text-align: center;
}

.example-sentence {
	line-height: 1.5;
	margin-top: 50px;
	cursor: default;
}

.show-buttons {
	display: flex;
	justify-content: space-between;
	margin-top: 100px;
}

.translations {
	margin-top: 50px;
  list-style-type: none;
  padding: 0;

	li {
		color: $background-100;
		background-color: $foreground-95;
	  margin: 5px 0;
	  padding: 10px;
	  border-radius: 5px;
	}
}


.response-buttons {
	margin: 50px -5px 0 -5px;
  display: flex;
  justify-content: space-between;

  button {
		margin: 0 5px;
	}

}

.done {
	text-align: center;
	margin-top: 150px;
}
</style>
