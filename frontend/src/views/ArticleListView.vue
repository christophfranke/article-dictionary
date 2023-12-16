<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

import type { ArticlePreview } from '@/types';
import { useFetchAuthorized } from '@/use/api';

import ArticlePreviewComponent from '@/components/ArticlePreview.vue';
import ProgresseComponent from '@/components/Progress.vue';

import Headline from '@/elements/Headline.vue';
import ButtonLink from '@/elements/ButtonLink.vue';


const articles = ref<ArticlePreview[]>([]);
const router = useRouter();

const newestArticles = computed(() =>
  articles.value
    .filter(article => article.owned)
    .sort((a, b) =>
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
    );

const usefulness = (article: ArticlePreview): number =>
  (0.2 * article.statistics.known.cluster
    + 1.0 * article.statistics.seen.cluster
    - 0.5 * article.statistics.new.cluster)
  / article.statistics.total;


const publicArticles = computed(() =>
  articles.value
    .filter(article => !article.owned)
    .sort((a, b) => usefulness(b) - usefulness(a))
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
      <Headline>Your Articles</Headline>
      <ButtonLink to="/create" class="create-link">Create New Article</ButtonLink>
    </div>
    <div v-if="newestArticles.length > 0" class="article-list">
      <ArticlePreviewComponent v-for="article in newestArticles" :key="article.id" :article="article" />
    </div>

    <div v-else class="no-articles">
      <p>No articles available.</p>
    </div>

    <template v-if="publicArticles.length > 0">
      <div class="title">
        <Headline>Public Articles</Headline>
      </div>
      <div class="article-list">
        <ArticlePreviewComponent v-for="article in publicArticles" :key="article.id"  :article="article" />
      </div>
    </template>
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
  margin-bottom: 20px;
  margin-top: 40px;
}

.article-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.no-articles {
  font-size: 20px;
  text-align: center;
  margin: 20px 0;
}
</style>
