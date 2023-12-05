<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ArticlePreview from '../components/ArticlePreview.vue';

interface ArticleData {
  id: number;
  url: string;
  title: string;
  excerpt: string;
}

const articles = ref<ArticleData[]>([]);
const router = useRouter();

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
    <h1 class="main-heading">Articles</h1>

    <div v-if="articles.length > 0" class="article-list">
      <article v-for="article in articles" :key="article.id" class="article-preview">
        <ArticlePreview :data="article" />
      </article>
    </div>

    <div v-else class="no-articles">
      <p>No articles available.</p>
    </div>

    <router-link to="/create" class="create-link">Create Article</router-link>
  </main>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.main-heading {
  font-size: 2em;
  color: #333;
  margin-bottom: 20px;
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
