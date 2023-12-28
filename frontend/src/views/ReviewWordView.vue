<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import type { WordDetail, PartialWord } from '@/types';
import { useDictionaryView } from '@/use/dictionary';
import useReview from '@/use/review';

import ProcessedContent from '@/components/ProcessedContent.vue';
import Tooltip from '@/components/Tooltip.vue';

import Headline from '@/elements/Headline.vue';
import Paragraph from '@/elements/Paragraph.vue';
import Button from '@/elements/Button.vue';

const contentDisplay = {
  padding: true,
  click: false,
  highlight: {
    new: false,
    seen: false,
    mark: true,
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

const recentlyShown: string[] = [];
const { dictionary, isLoading } = useDictionaryView(
	word => !recentlyShown.includes(word.id)
);
const { pickSentence, findWordForReview } = useReview(dictionary);
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

const highlight = ref({ word: '', index: -1});
const sanitizedHighlight = computed(() => {
	return !highlight.value || highlight.value?.word === word.value?.original
		? { word: '', index: -1 }
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
type Response = {
	label: string,
	fn: LevelFn,
}
const responses: { [key: string]: Response } = {
	'1': {
		label: 'No chance',
		fn: level => 1,
	},
	'2': {
		label: 'Almost',
		fn: level => level - 1,
	},
	'3': {
		label: 'Barely',
		fn: level => level,
	} ,
	'4': {
		label: 'Got it',
		fn: level => level + 1,
	},
	'5': {
		label: 'Too easy',
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

const setIgnore = () => {
	if (word.value) {
		dictionary.updateOne(word.value.id, { status: 'ignore' });	
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

onMounted(async () => {
  document.addEventListener('keydown', handleKeyPress);

  if (!dictionary.items.value.length) {
		await dictionary.load();
	}

  if (!wordId.value) {
	  wordId.value = findWordForReview();
  }
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyPress);
});
</script>


<template>
	<div class="container">
		<div v-if="!word">
			<Headline type="h2">Loading...</Headline>
		</div>
	  <div class="flashcard" v-else>
	      <Headline class="original" type="h2">{{ word.original }}</Headline>
	      <Paragraph class="example-sentence" v-if="sentence">
	      	<ProcessedContent :content="sentence.text" :words="sentence.words" :dictionary="dictionary" :mark="word.original" :display="contentDisplay" v-model="highlight" :key="word.id" />
	      </Paragraph>
	    <div v-if="phase === 'recall'">
	      <div class="show-buttons">
	      	<Button @click="setIgnore"><FontAwesomeIcon icon="ban" /></Button>
		      <Button role="view" @click="showTranslation">Show Translation&nbsp;&#8629;</Button>
		      <Button role="view" @click="skipWord">
		      	Skip&nbsp;&#8594;
		      </Button>
		    </div>
	    </div>
	    <div v-else>
	      <ul class="translations">
	        <li v-for="translation in word.translations" :key="translation">{{ translation }}</li>
	      </ul>
	      <div class="response-buttons">
	      	<Button v-for="(response, key) in responses" :key="key" @click="recordResponse(key)">{{ response.label }} ({{ key }})</Button>
	      </div>
	      <div class="show-buttons">
	      	<Button @click="setIgnore"><FontAwesomeIcon icon="ban" /></Button>
		      <Button role="view" @click="skipWord">
		      	Skip&nbsp;&#8594;
		      </Button>
		    </div>
	    </div>
	  </div>
    <Tooltip :highlighted="sanitizedHighlight" :dictionary="dictionary" :display="tooltipDisplay" />
	</div>
</template>

<style scoped lang="scss">
@import '@/style/global.scss';

.container {
  max-width: 750px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 100px;
}


.flashcard {
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
</style>
