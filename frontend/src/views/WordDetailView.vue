<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useFetchAuthorized } from '@/use/api';
import type { WordDetail } from '@/types'
import ProcessedContent from '@/components/ProcessedContent.vue';


const word = ref<WordDetail | null>(null);
const fetchAuthorized = useFetchAuthorized();

const route = useRoute();
const original = route.params.original;

const fetchWord = async () => {
  const data = await fetchAuthorized<WordDetail>(`/api/dictionary/${original}`);

  if (data) {
	  word.value = data;
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
            <ProcessedContent :content="sentence.text" :words="sentence.words" :dictionary="null" />
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No sentences available.</p>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>
