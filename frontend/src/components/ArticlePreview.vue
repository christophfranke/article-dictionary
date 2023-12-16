<script setup lang="ts">
import { computed } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import type { ArticlePreview } from '@/types';

import Headline from '@/elements/Headline.vue';


const props = defineProps({
  article: {
    type: Object as unknown as () => ArticlePreview,
    required: true,
  }
});

const familiarityScore = computed<number>(() => {
  const total = props.article.statistics.seen.cluster
    + props.article.statistics.known.cluster
    + props.article.statistics.new.cluster;

  return Math.round(100 * (0.2 * props.article.statistics.seen.cluster
    + props.article.statistics.known.cluster
    + 0.05 * props.article.statistics.new.cluster) / total)
});

const difficultyScore = computed(() => 100 - familiarityScore.value);

const scoreDescription = computed(() => {
  if (familiarityScore.value < 50) {
    return 'Very Hard';
  } else if (familiarityScore.value < 62) {
    return 'Hard';
  } else if (familiarityScore.value < 74) {
    return 'Medium'
  } else if (familiarityScore.value < 86) {
    return 'Easy';
  } else if (familiarityScore.value < 98) {
    return 'Very Easy'
  } else {
    return 'Too Easy';
  }
});

const lengthDescription = computed(() => {
  if (props.article.statistics.total < 100) {
    return 'Very Short';
  } else if (props.article.statistics.total < 400) {
    return 'Short';
  } else if (props.article.statistics.total < 1000) {
    return 'Medium'
  } else if (props.article.statistics.total < 2000) {
    return 'Long';
  } else if (props.article.statistics.total < 5000) {
    return 'Very Long'
  } else {
    return 'Epic';
  }

});

const link = (article: ArticlePreview): string => article.owned
  ? `/articles/${article.slug}`
  : `/articles/import/${article.id}`

</script>

<template>
  <div class="outer-container">
    <div class="article-preview">
      <router-link :to="link(props.article)">
        <Headline type="h3" class="title">{{ props.article.title }}</Headline>
        <p>{{ props.article.excerpt }}...</p>
        <div class="statistics">
          <span style="color: #666;" :title="`${props.article.statistics.new.words} new words`">
            <FontAwesomeIcon icon="sun" /> {{ props.article.statistics.new.words }}
          </span>
          <span style="color: #666;" :title="`${props.article.statistics.seen.words} seen words`">
            <FontAwesomeIcon icon="eye" /> {{ props.article.statistics.seen.words }}
          </span>
          <span style="color: #666;" :title="`${props.article.statistics.known.words} known words`">
            <FontAwesomeIcon icon="circle-check" /> {{ props.article.statistics.known.words }}
          </span>
        </div>

        <div class="difficulty">
          <div class="left" :title="`Estimated difficulty: ${scoreDescription} (${difficultyScore}% unknown words)`">
            <span>{{ scoreDescription }}</span>
            <span><FontAwesomeIcon icon="lightbulb" /></span>
            <span>{{ difficultyScore }}%</span>
          </div>
          <div class="right" :title="`${props.article.statistics.total} words total`">
            <span>{{ props.article.statistics.total }}</span>
            <span><FontAwesomeIcon icon="database" /></span>
            <span>{{ lengthDescription }}</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.outer-container {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  padding: 15px;
  padding-bottom: 27px;
  border-radius: 8px;
}

.article-preview {
  background-color: #fff; /* Bright background color */
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  height: calc(100% - 30px);
  padding: 20px;
}

.article-preview:hover {
  transform: translateY(-5px);
}

.article-preview > a {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.title {
  margin-bottom: 10px;
}

p {
  color: #666; /* Slightly darker text color */
  margin: 0;
  margin-bottom: 30px;
}

.statistics {
  margin-top: auto;
  color: #666;
  display: flex;
  justify-content: space-between;
}

.difficulty {
  font-size: 14px;
  margin-top: 15px;
  color: #666;
  display: flex;
  justify-content: space-between;
}

.difficulty .left span {
  padding-right: 5px;
}

.difficulty .right span {
  padding-left: 5px;
}


a:hover {
  background-color: transparent;
}
</style>
