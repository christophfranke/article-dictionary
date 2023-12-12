<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

import type { ArticlePreview } from '@/types';
import { useFetchAuthorized } from '@/use/api';

import ArticlePreviewComponent from '../components/ArticlePreview.vue';
import ProgresseComponent from '../components/Progress.vue';


const articles = ref<ArticlePreview[]>([]);
const router = useRouter();

const newestArticles = computed(() =>
  [...articles.value].sort((a, b) =>
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
  );

const fetchAuthorized = useFetchAuthorized();
const fetchArticles = async (): Promise<void> => {
  const data = await fetchAuthorized<ArticlePreview[]>('/api/articles/');
  if (data) {
    articles.value = data;
  } else {
    console.error('Failed to fetch articles.');
  }
};

onMounted(() => {
  fetchArticles();
});

const navigateToCreateArticle = (): void => {
  router.push('/create');
};
</script>

<template>
  <main class="container">
    <div class="title">
      <h2>Articles</h2>
      <router-link to="/create" class="create-link">Create New Article</router-link>
    </div>
    <div v-if="newestArticles.length > 0" class="article-list">
      <article v-for="article in newestArticles" :key="article.id" class="article-preview">
        <ArticlePreviewComponent :article="article" />
      </article>
    </div>
    <div v-else class="no-articles">
      <p>No articles available.</p>
    </div>

    <router-link to="/create" class="create-link">Create New Article</router-link>
  </main>
</template>

<style scoped>
.container {
  max-width: 950px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 100px;
}

.title {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

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

.no-articles {
  text-align: center;
  margin: 20px 0;
}

.create-link {
  display: block;
  background-color: #007bff;
  color: #fff;
  text-align: center;
  padding: 10px;
  margin-top: 20px;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.create-link:hover {
  background-color: #0056b3;
}
</style>
