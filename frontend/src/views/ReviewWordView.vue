<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import type { WordDetail } from '@/types';
import { useDictionaryView } from '@/use/dictionary';

import Headline from '@/elements/Headline.vue';
import Button from '@/elements/Button.vue';


const { dictionary, isLoading } = useDictionaryView();
const findWordForReview = (): WordDetail => {
	// Here you can implement your own logic to find a word for review
	const choice = Math.floor(dictionary.items.value.length * Math.random());
	return dictionary.items.value[choice] as WordDetail;
};

const word = ref<WordDetail>(findWordForReview());
const phase = ref('recall');

const showTranslation = () => {
  phase.value = 'review';
}

const recordResponse = (response: string) => {
  console.log(`User responded: ${response}`);
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
