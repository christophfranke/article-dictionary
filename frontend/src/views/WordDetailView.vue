<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import type { WordDetail } from '@/types'

import { useFetchAuthorized } from '@/use/api';
import { useDictionaryView } from '@/use/dictionary'
import { useToggleStatusSeen } from '@/use/toggle-status-seen';

import ProcessedContent from '@/components/ProcessedContent.vue';
import Tooltip from '@/components/Tooltip.vue';


const word = ref<WordDetail | null>(null);
const highlightedWord = ref('');
const fetchAuthorized = useFetchAuthorized();

const route = useRoute();
const original = computed(() => route.params.original);

const dictionary = useDictionaryView()
const toggleStatusSeen = useToggleStatusSeen(dictionary);

const fetchWord = async () => {
  const data = await fetchAuthorized<WordDetail>(`/api/dictionary/${original.value}`);

  if (data) {
    word.value = data;
  }
};

const contentDisplay = {
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
};

const router = useRouter()
const navigate = (word: string) => {
  router.push(`/dictionary/${word.toLowerCase()}`)
};



watchEffect(() => {
  fetchWord();
});
</script>

<template>
  <div class="main">
    <div v-if="word">
      <div class="stats">
        <h2>{{ word?.original }}</h2>
        <p><strong>Original:</strong> {{ word.original }}</p>
        <p><strong>Translations:</strong> {{ word.translations.join(', ') }}</p>
        <p><strong>Status:</strong> {{ word.status }}</p>
        <p><strong>Frequency:</strong> {{ word.frequency }}</p>
      </div>
      <div v-if="word.sentences.length > 0" class="sentences">
        <ul>
          <li v-for="(sentence, index) in word.sentences" :key="index">
            <ProcessedContent :content="sentence.text" :words="sentence.words" :dictionary="dictionary" :mark="word.original" :display="contentDisplay" v-model="highlightedWord"  @click="navigate" />
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No sentences available.</p>
      </div>
    </div>
    <Tooltip :dictionary="dictionary" :highlightedWord="highlightedWord" :display="tooltipDisplay" />
  </div>
</template>

<style scoped>
.main {
  font-family: 'Arial', sans-serif;
  font-size: 18px;
  max-width: 1000px;
  margin: 0 auto;
}

.stats {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.sentences {
  margin-top: 20px;
  padding: 20px;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
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
