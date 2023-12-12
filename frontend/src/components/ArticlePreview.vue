<script setup lang="ts">
import { computed } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import type { ArticlePreview } from '@/types';

interface Props {
  article: ArticlePreview
}

const props = defineProps({
  article: {
    type: Object,
    required: true,
  }
});

const familiarityScore = computed(() => {
  const total = props.article.statistics.seen
    + props.article.statistics.known
    + props.article.statistics.new;

  return Math.round(100 * (0.2 * props.article.statistics.seen
    + props.article.statistics.known
    + 0. * props.article.statistics.new) / (total))
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
  <div class="article-preview">
    <router-link :to="link(props.article)">
      <h2>{{ props.article.title }}</h2>
      <p>{{ props.article.excerpt }}...</p>
      <div class="statistics">
        <span style="color: #666;" :title="`${props.article.statistics.new} new words`">
          <FontAwesomeIcon icon="sun" /> {{ props.article.statistics.new }}
        </span>
        <span style="color: #666;" :title="`${props.article.statistics.seen} seen words`">
          <FontAwesomeIcon icon="eye" /> {{ props.article.statistics.seen }}
        </span>
        <span style="color: #666;" :title="`${props.article.statistics.known} known words`">
          <FontAwesomeIcon icon="circle-check" /> {{ props.article.statistics.known }}
        </span>
      </div>

      <div class="difficulty">
        <div class="left" :title="`Estimated difficulty: ${scoreDescription} (${difficultyScore}%)`">
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
</template>

<style scoped>
.article-preview {
  background-color: #fff; /* Bright background color */
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  height: calc(100% - 30px);
}

.article-preview:hover {
  transform: translateY(-5px);
}

.article-preview > a {
  height: 100%;
  display: flex;
  flex-direction: column;
}

h2 {
  color: #333; /* Dark font color */
  margin-top: 0;
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
