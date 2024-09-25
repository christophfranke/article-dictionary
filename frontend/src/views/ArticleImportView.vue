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
    <div class="container">
        <Headline class="title">{{ __('Importing article...') }}</Headline>
        <Paragraph>{{ __('This may take a minute.') }}</Paragraph>
        <ErrorMessage :message="errorMessage" />
    </div>
</template>


<style scoped>
.container {
  width: 80vw;
  max-width: 1200px;
	margin: 80px auto;
}

.title {
	text-align: center;
}
</style>