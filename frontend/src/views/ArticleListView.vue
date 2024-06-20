<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

import type { ArticlePreview } from '@/types';
import useApi from '@/use/api';

import { useArticleView } from '@/use/articles';

import ArticlePreviewComponent from '@/components/ArticlePreview.vue';

import Headline from '@/elements/Headline.vue';
import ButtonLink from '@/elements/ButtonLink.vue';

import __ from '@/i18n'


const { articles, isLoading } = useArticleView();
const router = useRouter();

const newestArticles = computed(() =>
  articles.previews.value
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
  articles.previews.value
    .filter(article => !article.owned)
    .sort((a, b) => usefulness(b) - usefulness(a))
  );

const navigateToCreateArticle = (): void => {
  router.push('/create');
};

onMounted(() => {
  articles.load()
});
</script>

<template>
  <main class="container">
    <template v-if="isLoading && !articles.previews.value.length">
      <Headline type="h2">{{ __('Loading Articles...') }}</Headline>
    </template>
    <template v-else>
      <div class="title">
        <Headline>{{ __('Your Articles') }}</Headline>
        <ButtonLink to="/create" class="create-link">{{ __('Create New Article') }}</ButtonLink>
      </div>
      <div v-if="newestArticles.length > 0" class="article-list">
        <ArticlePreviewComponent v-for="article in newestArticles" :key="article.id" :article="article as any" />
      </div>

      <div v-else class="no-articles">
        <p>{{ __('No articles available.') }}</p>
      </div>

      <template v-if="publicArticles.length > 0">
        <div class="title">
          <Headline>{{ __('Public Articles') }}</Headline>
        </div>
        <div class="article-list">
          <ArticlePreviewComponent v-for="article in publicArticles" :key="article.id" :article="article as any" />
        </div>
      </template>
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
