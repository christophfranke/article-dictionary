<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

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
const original = route.params.original;

const dictionary = useDictionaryView()
const toggleStatusSeen = useToggleStatusSeen(dictionary);

const fetchWord = async () => {
  const data = await fetchAuthorized<WordDetail>(`/api/dictionary/${original}`);

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



onMounted(() => {
  fetchWord();
});
</script>

<template>
  <div>
    <h2>Word Details</h2>
    <div v-if="word">
      <p><strong>Original:</strong> {{ word.original }}</p>
      <p><strong>Translations:</strong> {{ word.translations.join(', ') }}</p>
      <p><strong>Status:</strong> {{ word.status }}</p>
      <p><strong>Frequency:</strong> {{ word.frequency }}</p>
      <div v-if="word.sentences.length > 0">
        <strong>Sentences:</strong>
        <ul>
          <li v-for="(sentence, index) in word.sentences" :key="index">
            <ProcessedContent :content="sentence.text" :words="sentence.words" :dictionary="dictionary" :mark="word.original" :display="contentDisplay" v-model="highlightedWord" />
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
