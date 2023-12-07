<script setup lang="ts">
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
</script>

<template>
  <div class="article-preview">
    <router-link :to="`/articles/${props.article.slug}`">
      <h2>{{ props.article.title }}</h2>
      <p>{{ props.article.excerpt }}...</p>
      <div class="statistics">
        <span style="color: #666;">
          <FontAwesomeIcon icon="plus" /> {{ props.article.statistics.new }}
        </span>
        <span style="color: #666;">
          <FontAwesomeIcon icon="eye" /> {{ props.article.statistics.seen }}
        </span>
        <span style="color: #666;">
          <FontAwesomeIcon icon="check" /> {{ props.article.statistics.known }}
        </span>
        <span style="color: #666;">
          <FontAwesomeIcon icon="globe" /> {{ props.article.statistics.total }}
        </span>
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

a:hover {
  background-color: transparent;
}
</style>
