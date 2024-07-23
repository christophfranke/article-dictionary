<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import type { WordDetail, Token, Highlight } from '@/types'

import useApi from '@/use/api';
import { useDictionaryView } from '@/use/dictionary'
import { useToggleStatusSeen } from '@/use/toggle-status-seen';
import useTime from '@/use/time';
import { calculateIdealReviewInterval } from '@/use/review';
import useWordCache from '@/use/word-cache';

import NotFoundView from '@/views/NotFoundView.vue';

import ProcessedContent from '@/components/ProcessedContent.vue';
import Tooltip from '@/components/Tooltip.vue';

import Headline from '@/elements/Headline.vue';
import Paragraph from '@/elements/Paragraph.vue';

import __ from '@/i18n'


const word = ref<WordDetail | null>(null);
const isLoading = ref<boolean>(true);
const highlighted = ref<Highlight>({
  token: null,
  index: -1
});
const { fetchAuthorized } = useApi();

const route = useRoute();
const original = computed(() => typeof route.params.original === 'string' ? route.params.original : route.params.original[0]);

const { dictionary } = useDictionaryView()
const toggleStatusSeen = useToggleStatusSeen(dictionary);

const { timeAgo, describeTimeInterval } = useTime();
const reviewIntervalDescription = computed(() => {
  if (!word.value) {
    return '';
  }

  const interval = calculateIdealReviewInterval(word.value.reviewLevel);
  if (!interval) {
    return 'no review';
  }
  return `every ${describeTimeInterval(interval)}`;
});

const tokanize = (word: string): Token => {
  return {
    display: word,
    word: word,
    space: ', ',
    ignore: false
  }
}


const wordCache = useWordCache()
const fetchWord = async () => {
  // try cache first
  const newWord: string = original.value
  word.value = wordCache.get(newWord)
  isLoading.value = false

  if (!word.value) {
    isLoading.value = true
    const data = await fetchAuthorized<WordDetail>(`/api/dictionary/${newWord}`);

    if (data) {
      if (newWord === original.value) {
        word.value = data;
      }
      wordCache.add(newWord, data)
    }

    if (newWord === original.value) {
      isLoading.value = false
    }
  }
};

const contentDisplay = {
  padding: true,
  click: true,
  highlight: {
    new: false,
    seen: false,
    mark: true,
  }
};

const similarDisplay = {
  padding: true,
  click: true,
  highlight: {
    new: false,
    seen: false,
    mark: false,
  }
}

const tooltipDisplay = {
  new: true,
  seen: true,
  known: true,
  update: {
    seen: false
  }
};

const router = useRouter()
const navigate = (params: { word: string }) => {
  highlighted.value.token = null
  highlighted.value.index = -1
  router.push(`/dictionary/${params.word}`)
};


watchEffect(() => {
  fetchWord();
});
</script>

<template>
  <div class="main">
    <div class="loading" v-if="isLoading">
      {{ __('Loading $1...', original) }}
    </div>
    <div v-if="!isLoading && word">
      <div class="stats">
        <Headline type="h2" class="headline">{{ word?.original }}</Headline>
        <p><strong>{{ __('Original') }}:</strong> {{ word.original }}</p>
        <p><strong>{{ __('Translations') }}:</strong> {{ word.translations.join(', ') }}</p>
        <p><strong>{{ __('Status') }}:</strong> {{ word.status }}</p>
        <p><strong>{{ __('Review level') }}:</strong> {{ word.reviewLevel }} ({{ reviewIntervalDescription }})</p>
        <p><strong>{{ __('Last seen') }}:</strong> {{ timeAgo(word.lastViewed) }}</p>
        <p><strong>{{ __('Frequency') }}:</strong> {{ word.frequency }}</p>
        <p><strong>{{ __('Similar words') }}:</strong>&nbsp;
          <ProcessedContent v-if="word.similar.length > 0" :tokens="word.similar.map(tokanize)" :dictionary="dictionary" :display="similarDisplay" v-model="highlighted" @click="navigate" :key="word.original" />
          <span v-else>{{ __('None') }}</span>
        </p>
      </div>
      <div v-if="word.sentences.length > 0" class="sentences">
        <ul>
          <li><strong>{{ __('Sentences') }}:</strong></li>
          <li v-for="(sentence, index) in word.sentences" :key="`${word.id}-${index}`">
            <Paragraph>
              <ProcessedContent :content="sentence.text" :tokens="sentence.tokens" :dictionary="dictionary" :mark="word.original" :display="contentDisplay" v-model="highlighted" @click="navigate" />
            </Paragraph>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>{{ __('No sentences available.') }}</p>
      </div>
    </div>
    <Tooltip :dictionary="dictionary" :highlighted="highlighted" :display="tooltipDisplay" />
  </div>
  <NotFoundView v-if="!isLoading && !word" />
</template>


<style scoped>
.main {
  font-size: 18px;
  max-width: 1000px;
  margin: 0 auto;
}

.loading {
  margin-top: 50px;
}

.headline {
  margin-bottom: 20px;
}


.stats {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.sentences {
  padding: 20px;
}

p {
  margin-bottom: 10px;
}

strong {
  font-weight: bold;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  margin-bottom: 25px;
}

.no-sentences {
  color: #888;
}
</style>
