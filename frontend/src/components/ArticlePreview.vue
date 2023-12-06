<script setup lang="ts">
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
    </router-link>
  </div>
</template>

<style scoped>
.article-preview {
  background-color: #fff; /* Bright background color */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.article-preview:hover {
  transform: translateY(-5px);
}

h2 {
  color: #333; /* Dark font color */
  margin-bottom: 10px;
}

p {
  color: #666; /* Slightly darker text color */
  margin: 0;
}
a:hover {
  background-color: transparent;
}
</style>
