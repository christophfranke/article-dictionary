<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import type { WordDetail } from '@/types'

import { useFetchAuthorized } from '@/use/api';
import { useDictionaryView } from '@/use/dictionary'
import { useToggleStatusSeen } from '@/use/toggle-status-seen';

import ProcessedContent from '@/components/ProcessedContent.vue';
import Tooltip from '@/components/Tooltip.vue';

import Headline from '@/elements/Headline.vue';
import Paragraph from '@/elements/Paragraph.vue';


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
const navigate = (word: string) => {
  router.push(`/dictionary/${word}`)
};


watchEffect(() => {
  fetchWord();
});
</script>

<template>
  <div class="main">
    <div v-if="word">
      <div class="stats">
        <Headline type="h2" class="headline">{{ word?.original }}</Headline>
        <p><strong>Original:</strong> {{ word.original }}</p>
        <p><strong>Translations:</strong> {{ word.translations.join(', ') }}</p>
        <p><strong>Status:</strong> {{ word.status }}</p>
        <p><strong>Frequency:</strong> {{ word.frequency }}</p>
        <p><strong>Similar words:</strong>&nbsp;
          <ProcessedContent v-if="word.similar.length > 0" :words="word.similar" :dictionary="dictionary" :display="similarDisplay" v-model="highlightedWord" @click="navigate" :key="word.original" />
          <span v-else>None</span>
        </p>
      </div>
      <div v-if="word.sentences.length > 0" class="sentences">
        <ul>
          <li><strong>Sentences:</strong></li>
          <li v-for="(sentence, index) in word.sentences" :key="`${word.id}-${index}`">
            <Paragraph>
              <ProcessedContent :content="sentence.text" :words="sentence.words" :dictionary="dictionary" :mark="word.original" :display="contentDisplay" v-model="highlightedWord" @click="navigate" />
            </Paragraph>
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
  font-size: 18px;
  max-width: 1000px;
  margin: 0 auto;
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
