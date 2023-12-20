<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

import type { ArticlePreview } from '@/types';
import useApi from '@/use/api';

import { useArticleView } from '@/use/articles';

import ArticlePreviewComponent from '@/components/ArticlePreview.vue';
import ArticlePreviewList from '@/components/ArticlePreviewList.vue';
import ProgresseComponent from '@/components/Progress.vue';

import Headline from '@/elements/Headline.vue';
import ButtonLink from '@/elements/ButtonLink.vue';

const { articles, isLoading } = useArticleView();
const router = useRouter();

const continueReadingArticlesCount = ref(3)
const continueReadingArticles = computed(() => {
  const sortedArticles = articles.previews.value
    .filter(article => article.owned)
    .filter(article => article.status === 'seen')
    .sort((a, b) => {
      return new Date(b.lastRead).getTime() - new Date(a.lastRead).getTime();
    });

  return sortedArticles.slice(0, continueReadingArticlesCount.value);
});

const usefulness = (article: ArticlePreview): number =>
  (0.2 * article.statistics.known.words
    + 1.0 * article.statistics.seen.words
    - 0.5 * article.statistics.new.words)
  / article.statistics.total;

const suggestedArticlesCount = ref(6)
const suggestedArticles = computed(() => {
  const baseArticles = articles.previews.value
    .filter(article => article.owned)
    .filter(article => article.status !== 'read')

  const sortedArticles = baseArticles.sort((a, b) => usefulness(b) - usefulness(a));
  return sortedArticles.slice(0, suggestedArticlesCount.value);
});

const newArticlesCount = ref(6)
const newArticles = computed(() => {
  const baseArticles = articles.previews.value
    .filter(article => article.owned)
    .filter(article => article.status === 'new')

  const sortedArticles = baseArticles.sort((a, b) => {
    return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
  });

  return sortedArticles.slice(0, newArticlesCount.value);
});


const readArticlesCount = ref(6)
const readArticles = computed(() => {
  const baseArticles = articles.previews.value
    .filter(article => article.owned)
    .filter(article => article.status === 'read')

  const sortedArticles = baseArticles.sort((a, b) => usefulness(b) - usefulness(a));
  return sortedArticles.slice(0, readArticlesCount.value);
});

const remainingArticles = computed(() => {
  const baseArticles = articles.previews.value
    .filter(article => article.owned)
    .filter(article => !continueReadingArticles.value.includes(article))
    .filter(article => !suggestedArticles.value.includes(article))
    .filter(article => !newArticles.value.includes(article))
    .filter(article => !readArticles.value.includes(article))

  const sortedArticles = baseArticles.sort((a, b) => usefulness(b) - usefulness(a));
  return sortedArticles
});

const publicArticlesCount = ref(9)
const publicArticles = computed(() => {
  const baseArticles = articles.previews.value
    .filter(article => !article.owned)

  const sortedArticles = baseArticles.sort((a, b) => usefulness(b) - usefulness(a));
  return sortedArticles.slice(0, publicArticlesCount.value);
})


const navigateToCreateArticle = (): void => {
  router.push('/create');
};
</script>

<template>
  <main class="container">
    <ProgresseComponent />

    <template v-if="isLoading && !articles.previews.value.length">
      <div class="no-articles">
        <Headline class="title">Loading...</Headline>
      </div>
    </template>
    <template v-else>
      <div v-if="articles.previews.value.length === 0" class="no-articles">
        <Headline class="title">You have no articles yet.</Headline>
        <ButtonLink to="/create" class="create-link">Create New Article</ButtonLink>
      </div>

      <ArticlePreviewList
        title="Continue Reading"
        :articleList="continueReadingArticles" />

      <ArticlePreviewList
        title="Suggested Articles"
        :articleList="suggestedArticles" />

      <ArticlePreviewList
        title="New Articles"
        :articleList="newArticles" />

      <ArticlePreviewList
        title="Public Articles"
        :articleList="publicArticles"
        :showCreateButton="false" />

      <ArticlePreviewList
        title="Read again"
        :articleList="readArticles" />

      <ArticlePreviewList
        title="More Articles"
        :articleList="remainingArticles" />
    </template>
  </main>
</template>

<style scoped lang="scss">
.container {
  max-width: 950px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 100px;
}

.no-articles {
  text-align: center;
  margin: 100px 0;

  .title {
    margin: 50px 0;
  }
}


.create-link {
  margin: 20px auto;
}
</style>
