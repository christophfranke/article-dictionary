<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import useApi from '@/use/api';
import type { ArticleDetail } from '@/types'
import { useArticleView } from '@/use/articles';

import ErrorMessage from '@/elements/ErrorMessage.vue';
import Paragraph from '@/elements/Paragraph.vue';
import Headline from '@/elements/Headline.vue';

import __ from '@/i18n'


const route = useRoute();
const id = route.params.id as string;

const router = useRouter();

const { articles, errorMessage } = useArticleView();
const importArticle = async () => {
  const newArticle = await articles.add({ id });

  if (newArticle) {
    router.push(`/articles/${newArticle.slug}`);
  }
}

onMounted(importArticle)

</script>

<template>
    <Headline class="title">{{ __('Importing article...') }}</Headline>
    <Paragraph>{{ __('Translating the article word by word. This may take a minute.') }}</Paragraph>
    <ErrorMessage :message="errorMessage" />
</template>


<style scoped>
.title {
	margin: 80px auto;
	text-align: center;
}
</style>