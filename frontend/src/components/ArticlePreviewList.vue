<script setup lang="ts">
import type { ArticlePreview } from '@/types';
import ArticlePreviewComponent from '@/components/ArticlePreview.vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  articleList: {
    type: Array as unknown as () => ArticlePreview[],
    required: true,
  },
  showCreateButton: {
    type: Boolean,
    default: true
  }
})
</script>

<template>
  <template v-if="props.articleList.length > 0">
    <h2>{{ props.title }}</h2>
    <div class="article-list">
      <article v-for="article in props.articleList" :key="article.id" class="article-preview">
        <ArticlePreviewComponent :article="article" />
      </article>
    </div>

    <router-link v-if="props.showCreateButton" to="/create" class="create-link">Create New Article</router-link>
  </template>
</template>

<style scoped>
.article-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.article-preview {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
}

.create-link {
  display: block;
  background-color: #007bff;
  color: #fff;
  text-align: center;
  padding: 10px;
  margin: 20px auto;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.create-link:hover {
  background-color: #0056b3;
}
</style>