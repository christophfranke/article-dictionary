<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import type { WordDetail, PartialWord } from '@/types';
import { useDictionaryView } from '@/use/dictionary';

import Headline from '@/elements/Headline.vue';
import Button from '@/elements/Button.vue';


const { dictionary, isLoading } = useDictionaryView();
const findWordForReview = (): WordDetail => {
  const now = new Date();

	const maxFreq = Math.max(...dictionary.items.value.map(word => word.frequency));
	const calculateImportance = (word: PartialWord): number => {
		const frequency = word.frequency
	  if (frequency === 0) return 0;
	  if (maxFreq === 1) return 1; // Edge case to handle if maxFreq is 1

	  // Logarithmic scale: importance goes from 0 (for freq 1) to 1 (for maxFreq)
	  return Math.log(frequency) / Math.log(maxFreq);
	};

  const calculateScore = (word: PartialWord): number => {
    const lastViewed = new Date(word.lastViewed);
    const timeSinceLastViewed = (now.getTime() - lastViewed.getTime()) / (1000 * 3600 * 24); // in days

    if (word.reviewLevel === 0) {
      return 0;
    }

    // wait for at least 3 minutes before reviewing again
    if (timeSinceLastViewed < 3 / (24 * 60)) {
			return 0;
		}

    if (word.reviewLevel === 1) {
      return (1 - timeSinceLastViewed) / 1; // 1 day
    }

    // Calculate ideal review time
    const idealReviewTime = 3.5 * Math.pow(2, word.reviewLevel - 2); // level 2 -> 3.5 days, doubles with each level
    return timeSinceLastViewed * (2 - timeSinceLastViewed) / idealReviewTime;
  };

  let highestScore = -Infinity;
  let wordToReview: any | null = null;

  for (const word of dictionary.items.value) {
    const score = calculateImportance(word) * calculateScore(word);
    if (score > highestScore) {
    	console.log(`Found new highest score for ${word.original}: ${score}`);
      highestScore = score;
      wordToReview = word;
    }
  }

  return wordToReview
};

const word = ref<WordDetail>(findWordForReview());
const phase = ref('recall');

const showTranslation = () => {
	dictionary.markSeen(word.value.id);
  phase.value = 'review';
}

const recordResponse = async (response: string) => {
  console.log(`User responded: ${response}`);

  let reviewLevel = word.value.reviewLevel
  switch (response) {
		case 'again':
			reviewLevel = 1;
			break;
		case 'hard':
			reviewLevel--;
			break;
		case 'good':
			reviewLevel++;
			break;
		case 'easy':
			reviewLevel += 2;
			break;
	}

	if (reviewLevel < 1) {
		reviewLevel = 1;
	}

	await dictionary.updateOne(word.value.id, { reviewLevel });

  word.value = findWordForReview();
  phase.value = 'recall';
}

const handleKeyPress = (event: KeyboardEvent) => {
  if (phase.value === 'recall' && event.key === 'Enter') {
    showTranslation();
  } else if (phase.value === 'review') {
    switch(event.key) {
      case '1': recordResponse('again'); break;
      case '2': recordResponse('hard'); break;
      case '3': recordResponse('good'); break;
      case '4': recordResponse('easy'); break;
    }
  }
}

onMounted(async () => {
  document.addEventListener('keydown', handleKeyPress);

  await dictionary.load();
  if (!word.value) {
	  word.value = findWordForReview();
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
	    <div v-if="phase === 'recall'">
	      <Headline class="original" type="h2">{{ word.original }}</Headline>
	      <div class="show-translation">
		      <Button type="view" @click="showTranslation">Show Translation (Press Enter)</Button>
		    </div>
	    </div>
	    <div v-else>
	      <Headline class="original" type="h2">{{ word.original }}</Headline>
	      <ul class="translations">
	        <li v-for="translation in word.translations" :key="translation">{{ translation }}</li>
	      </ul>
	      <div class="response-buttons">
	        <Button @click="recordResponse('again')">Again (1)</Button>
	        <Button @click="recordResponse('hard')">Hard (2)</Button>
	        <Button @click="recordResponse('good')">Good (3)</Button>
	        <Button @click="recordResponse('easy')">Easy (4)</Button>
	      </div>
	    </div>
	  </div>
	</div>
</template>

<style scoped lang="scss">
@import '@/style/global.scss';

.container {
  max-width: 600px;
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

.show-translation {
	text-align: center;
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
	margin-bottom: 0;
	margin-top: 50px;
  display: flex;
  justify-content: space-between;
  width: 100%;
}
</style>
