<script setup lang="ts">
import { ref } from 'vue';

import type { Article } from '../types'
import type { DictionaryCollection } from '../dictionary/collection';

import useStatistics from '../use/statistics';

const { dictionary, article, showPercentage } = defineProps({
  dictionary: {
    type: Object as () => DictionaryCollection,
    required: true,
  },
  article: {
    type: Object as () => Article,
    default: undefined,
  },
  showPercentage: {
    type: Boolean,
    default: false,
  },
});

const statistics = useStatistics({ dictionary, article: article && ref(article) });
</script>

<template>
  <div class="statistics">
    <h3 v-if="article">Words in this article</h3>
    <h3 v-else>Word in dictionary</h3>
    <div class="word-statistics">
      <div class="word-statistic">
        <strong v-if="showPercentage">{{ statistics.newWordsPercentage }}%</strong>
        <strong v-else>{{ statistics.newWords }}</strong>
        <span>New</span>
      </div>
      <div class="word-statistic">
        <strong v-if="showPercentage">{{ statistics.seenWordsPercentage }}%</strong>
        <strong v-else>{{ statistics.seenWords }}</strong>
        <span>Seen</span>
      </div>
      <div class="word-statistic">
        <strong v-if="showPercentage">{{ statistics.knownWordsPercentage }}%</strong>
        <strong v-else>{{ statistics.knownWords }}</strong>
        <span>Known</span>
      </div>
      <div class="word-statistic total">
        <strong>{{ statistics.totalWords }}</strong>
        <span>Total</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.statistics {
  text-align: right;
  font-size: 16px;
  font-weight: normal;
}

.word-statistics {
  margin-top: 5px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-around;
}

.word-statistic {
  margin-left: 10px;
  text-align: center;
}

.word-statistic.total {
  margin-left: 25px;
}

.word-statistic strong {
  font-size: 16px;
  color: #333;
}

.word-statistic span {
  font-size: 12px;
  display: block;
  white-space: nowrap;
  color: #666;
}
</style>
