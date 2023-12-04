<template>
  <main>
    <h1>Hello</h1>

    <div v-if="articles.length > 0">
      <article v-for="article in articles" :key="article.id">
        <Article :data="article" />
      </article>
    </div>

    <div v-else>
      <p>No articles available.</p>
    </div>

    <router-link to="/create">Create Article</router-link>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Article from '../components/Article.vue'

const articles = ref<any[]>([]);

const router = useRouter();

const fetchArticles = async () => {
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

const navigateToCreateArticle = () => {
  router.push('/create');
};
</script>
