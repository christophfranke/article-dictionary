<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useArticleView } from '@/use/articles';

import type { ArticleData } from '@/types';

import Headline from '@/elements/Headline.vue';
import ArticleEditForm from '@/components/ArticleEditForm.vue'; // Import the new component

const article = ref<ArticleData | null>(null);

const route = useRoute();
const slug = ref<string>(typeof route.params.slug === 'string' ? route.params.slug : (route.params.slug[0] || ''));

const router = useRouter();
const { articles, errorMessage, isLoading } = useArticleView();

const submitForm = async (): Promise<void> => {
  if (article.value) {    
    const updatedArticle = await articles.updateOne(slug.value, article.value)

    if (updatedArticle) {
      router.push(`/articles/${updatedArticle.slug}`);
    }
  }
};

onMounted(async () => {
  article.value = await articles.get(slug.value);

  if (!article.value) {
    router.push('/404-not-found');
  }
});
</script>

<template>
  <div class="create-article" v-if="article">
    <Headline>Edit Article</Headline>
    <ArticleEditForm :article="article" :isLoading="isLoading" :errorMessage="errorMessage" @submit="submitForm" />
  </div>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

.create-article {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}
</style>
