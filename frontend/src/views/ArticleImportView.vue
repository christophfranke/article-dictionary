<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import useApi from '@/use/api';
import type { ArticleDetail } from '@/types'

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
	<h3>Importing article...</h3>
  <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
</template>

<style scoped>
h3 {
	margin: 80px auto;
	text-align: center;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
}
</style>