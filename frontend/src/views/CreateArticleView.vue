<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { useArticleView } from '@/use/articles';
import type { ArticleData } from '@/types';

import Headline from '@/elements/Headline.vue';
import ArticleEditForm from '@/components/ArticleEditForm.vue'; // Import the new component

import __ from '@/i18n'

const article = ref<ArticleData>({
  title: '',
  content: '',
  privacy: 'public',
});

const router = useRouter();
const { articles, errorMessage, isSending } = useArticleView();

const submitForm = async (): Promise<void> => {
  const newArticle = await articles.add(article.value);

  if (newArticle) {
    router.push(`/articles/${newArticle.slug}`);
  }
};
</script>

<template>
  <div class="create-article">
    <Headline>{{ __('Create Article') }}</Headline>
    <ArticleEditForm :article="article" :isLoading="isSending" :errorMessage="errorMessage" @submit="submitForm" />
  </div>
</template>


<style scoped lang="scss">
.create-article {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}
</style>
