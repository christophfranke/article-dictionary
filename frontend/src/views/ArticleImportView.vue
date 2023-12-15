<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import useApi from '@/use/api';
import type { ArticleDetail } from '@/types'

import ErrorMessage from '@/elements/ErrorMessage.vue';
import Headline from '@/elements/Headline.vue';


const route = useRoute();
const id = route.params.id;

const router = useRouter();

const { fetchAuthorized, errorMessage } = useApi();
const importArticle = async () => {
	const data = await fetchAuthorized<ArticleDetail>(`/api/articles/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id }),
  });

  if (data) {
  	router.push(`/articles/${data.slug}`)
  }
}

onMounted(importArticle)

</script>

<template>
	<Headline class="title">Importing article...</Headline>
  <ErrorMessage :message="errorMessage" />
</template>

<style scoped>
.title {
	margin: 80px auto;
	text-align: center;
}
</style>