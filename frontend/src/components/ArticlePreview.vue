<script setup lang="ts">
import { computed } from 'vue';
import type { PropType } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import type { ArticlePreview } from '@/types';

import Headline from '@/elements/Headline.vue';
import Excerpt from '@/elements/Excerpt.vue'

import __ from '@/i18n'

const props = defineProps({
  article: {
    type: Object as PropType<ArticlePreview>,
    required: true,
  }
});

const familiarityScore = computed<number>(() => {
  const total = props.article.statistics.seen.cluster
    + props.article.statistics.known.cluster
    + props.article.statistics.new.cluster;

  return Math.round(100 * (
    0.2 * props.article.statistics.seen.cluster
    + 1.0 * props.article.statistics.known.cluster
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
  if (props.article.statistics.total < 150) {
    return 'Very Short';
  } else if (props.article.statistics.total < 500) {
    return 'Short';
  } else if (props.article.statistics.total < 2000) {
    return 'Medium'
  } else if (props.article.statistics.total < 5000) {
    return 'Long';
  } else if (props.article.statistics.total < 10000) {
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
        <Excerpt class="excerpt">{{ props.article.excerpt }}...</Excerpt>
        <div class="statistics">
          <span :title="__('$1 new words', props.article.statistics.new.words)">
            <FontAwesomeIcon icon="sun" /> {{ props.article.statistics.new.words }}
          </span>
          <span :title="__('$1 seen words', props.article.statistics.seen.words)">
            <FontAwesomeIcon icon="eye" /> {{ props.article.statistics.seen.words }}
          </span>
          <span :title="__('$1 known words', props.article.statistics.known.words)">
            <FontAwesomeIcon icon="circle-check" /> {{ props.article.statistics.known.words }}
          </span>
        </div>

        <div class="difficulty">
          <div class="left" :title="__('Estimated difficulty: $1 ($2% unknown words)', scoreDescription, difficultyScore)">
            <span>{{ scoreDescription }}</span>
            <span><FontAwesomeIcon icon="lightbulb" /></span>
            <span>{{ difficultyScore }}%</span>
          </div>
          <div class="right" :title="__('$1 words total', props.article.statistics.total)">
            <span>{{ props.article.statistics.total }}</span>
            <span><FontAwesomeIcon icon="database" /></span>
            <span>{{ lengthDescription }}</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>


<style scoped lang="scss">
@import '@/style/global.scss';

.outer-container {
  background-color: $card-outer-background-color;
  border: 1px solid $border-color;
  padding: 15px;
  padding-bottom: 27px;
  border-radius: 8px;
}

.article-preview {
  background-color: $card-inner-background-color;
  border: 1px solid $border-color;
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
  color: inherit;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.title {
  margin-bottom: 10px;
}

.excerpt {
  margin: 0;
  margin-bottom: 30px;
}

.statistics {
  color: $statistics-preview-font-color;
  margin-top: auto;
  display: flex;
  justify-content: space-between;
}

.difficulty {
  color: $statistics-preview-font-color;
  font-size: 14px;
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
}

.difficulty .left span {
  padding-right: 5px;
}

.difficulty .right span {
  padding-left: 5px;
}

</style>
