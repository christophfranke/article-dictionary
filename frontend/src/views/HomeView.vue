<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

import type { ArticlePreview } from '@/types';
import { useFetchAuthorized } from '@/use/api';

import ArticlePreviewComponent from '../components/ArticlePreview.vue';
import ProgresseComponent from '../components/Progress.vue';


const articles = ref<ArticlePreview[]>([]);
const router = useRouter();

const continueReadingArticlesCount = ref(6)
const continueReadingArticles = computed(() => {
  const sortedArticles = articles.value
    .filter(article => article.status === 'seen')
    .sort((a, b) => {
      return new Date(b.lastRead).getTime() - new Date(a.lastRead).getTime();
    });

  return sortedArticles.slice(0, continueReadingArticlesCount.value);
});

const usefulness = (article: ArticlePreview): number => {
  return (1.0 * article.statistics.seen - 0.5 * article.statistics.new) / article.statistics.total;
}

const mostSeenWordsArticlesCount = ref(6)
const mostSeenWordsArticles = computed(() => {
  const baseArticles = articles.value
    .filter(article => !continueReadingArticles.value.includes(article))
    .filter(article => article.status !== 'read')

  const sortedArticles = baseArticles.sort((a, b) => usefulness(b) - usefulness(a));
  return sortedArticles.slice(0, mostSeenWordsArticlesCount.value);
});

const newestArticlesCount = ref(6)
const newestArticles = computed(() => {
  const baseArticles = articles.value
    .filter(article => !continueReadingArticles.value.includes(article))
    .filter(article => !mostSeenWordsArticles.value.includes(article))
    .filter(article => article.status === 'new')

  const sortedArticles = baseArticles.sort((a, b) => {
    return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
  });

  return sortedArticles.slice(0, newestArticlesCount.value);
});

const remainingArticles = computed(() => {
  const baseArticles = articles.value
    .filter(article => !continueReadingArticles.value.includes(article))
    .filter(article => !mostSeenWordsArticles.value.includes(article))
    .filter(article => !newestArticles.value.includes(article))

  const sortedArticles = baseArticles.sort((a, b) => usefulness(b) - usefulness(a));
  return sortedArticles
});


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
    <h2>Progress</h2>
    <ProgresseComponent />

    <div v-if="articles.length === 0" class="no-articles">
      <h3>You have no articles yet.</h3>
      <router-link to="/create" class="create-link">Create New Article</router-link>
    </div>

    <template v-if="continueReadingArticles.length > 0">
      <h2>Continue Reading</h2>
      <div class="article-list">
        <article v-for="article in continueReadingArticles" :key="article.id" class="article-preview">
          <ArticlePreviewComponent :article="article" />
        </article>
      </div>
    </template>

    <router-link v-if="continueReadingArticles.length > 0" to="/create" class="create-link">Create New Article</router-link>

    <template v-if="mostSeenWordsArticles.length > 0">
      <h2>New Articles</h2>
      <div class="article-list">
        <article v-for="article in mostSeenWordsArticles" :key="article.id" class="article-preview">
          <ArticlePreviewComponent :article="article" />
        </article>
      </div>
    </template>

    <router-link v-if="mostSeenWordsArticles.length > 0" to="/create" class="create-link">Create New Article</router-link>

    <template v-if="newestArticles.length > 0">
      <h2>New Articles</h2>
      <div class="article-list">
        <article v-for="article in newestArticles" :key="article.id" class="article-preview">
          <ArticlePreviewComponent :article="article" />
        </article>
      </div>
    </template>

    <router-link v-if="newestArticles.length > 0" to="/create" class="create-link">Create New Article</router-link>

    <template v-if="remainingArticles.length > 0">
      <h2>More Articles</h2>
      <div class="article-list">
        <article v-for="article in remainingArticles" :key="article.id" class="article-preview">
          <ArticlePreviewComponent :article="article" />
        </article>
      </div>
    </template>

    <router-link v-if="remainingArticles.length > 0" to="/create" class="create-link">Create New Article</router-link>
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
  margin: 50px 0;
}

.no-articles h3{
  margin: 70px 0;
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
