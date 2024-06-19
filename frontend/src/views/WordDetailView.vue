<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import type { WordDetail } from '@/types'

import { useFetchAuthorized } from '@/use/api';
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


const word = ref<WordDetail | null>(null);
const isLoading = ref<boolean>(true);
const highlighted = ref<{ word: string; index: number }>({
  word: '',
  index: -1
});
const fetchAuthorized = useFetchAuthorized();

const route = useRoute();
const original = computed(() => route.params.original);

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


const wordCache = useWordCache()
const fetchWord = async () => {
  // try cache first
  const newWord: string = typeof original.value === 'string' ? original.value : original.value[0]
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
  highlighted.value.word = ''
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
      Loading {{original}}...
    </div>
    <div v-if="!isLoading && word">
      <div class="stats">
        <Headline type="h2" class="headline">{{ word?.original }}</Headline>
        <p><strong>Original:</strong> {{ word.original }}</p>
        <p><strong>Translations:</strong> {{ word.translations.join(', ') }}</p>
        <p><strong>Status:</strong> {{ word.status }}</p>
        <p><strong>Review level:</strong> {{ word.reviewLevel }} ({{ reviewIntervalDescription }})</p>
        <p><strong>Last seen:</strong> {{ timeAgo(word.lastViewed) }}</p>
        <p><strong>Frequency:</strong> {{ word.frequency }}</p>
        <p><strong>Similar words:</strong>&nbsp;
          <ProcessedContent v-if="word.similar.length > 0" :words="word.similar" :dictionary="dictionary" :display="similarDisplay" v-model="highlighted" @click="navigate" :key="word.original" />
          <span v-else>None</span>
        </p>
      </div>
      <div v-if="word.sentences.length > 0" class="sentences">
        <ul>
          <li><strong>Sentences:</strong></li>
          <li v-for="(sentence, index) in word.sentences" :key="`${word.id}-${index}`">
            <Paragraph>
              <ProcessedContent :content="sentence.text" :words="sentence.words" :dictionary="dictionary" :mark="word.original" :display="contentDisplay" v-model="highlighted" @click="navigate" />
            </Paragraph>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No sentences available.</p>
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
