<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

import type { ArticlePreview } from '@/types';

import ArticlePreviewComponent from '../components/ArticlePreview.vue';
import ProgresseComponent from '../components/Progress.vue';


const articles = ref<ArticlePreview[]>([]);
const router = useRouter();

const latestArticles = computed(() => {
  const baseArticles = articles.value.filter(article => !newestArticles.value.includes(article))
  // const sortedArticles = articles.value.sort((a, b) => {
  //   return new Date(b.lastRead).getTime() - new Date(a.lastRead).getTime();
  // });

  return baseArticles.slice(0, 3);
})

const newestArticles = computed(() => {
  // const baseArticles = articles.value.filter(article => !latestArticles.value.includes(article))
  const baseArticles = articles.value
  // const sortedArticles = baseArticles.sort((a, b) => {
  //   return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
  // });

  return baseArticles.slice(0, 3);
})

const fetchArticles = async (): Promise<void> => {
  try {
    const response = await fetch('/api/articles/');
    if (response.ok) {
      articles.value = await response.json();
    } else {
      console.error('Failed to fetch articles:', response.status);
    }
  } catch (error) {
    console.error('Error fetching articles:', error);
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
    <h2>Progress</h2>
    <ProgresseComponent />

    <h2>Newest Articles</h2>
    <div v-if="newestArticles.length > 0" class="article-list">
      <article v-for="article in newestArticles" :key="article.id" class="article-preview">
        <ArticlePreviewComponent :article="article" />
      </article>
    </div>
    <router-link to="/create" class="create-link">Create New Article</router-link>

    <h2>Continue Reading</h2>
    <div v-if="latestArticles.length > 0" class="article-list">
      <article v-for="article in latestArticles" :key="article.id" class="article-preview">
        <ArticlePreviewComponent :article="article" />
      </article>
    </div>

    <div v-else class="no-articles">
      <p>No articles available.</p>
    </div>
  </main>
</template>

<style scoped>
.container {
  max-width: 950px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 100px;
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
