<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useFetchAuthorized } from '@/use/api';

const route = useRoute();
const id = route.params.id;

const router = useRouter();

const fetchAuthorized = useFetchAuthorized();
const importArticle = async () => {
	const data = await fetchAuthorized(`/api/articles/create`, {
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
</template>

<style scoped>
h3 {
	margin: 80px auto;
	text-align: center;
}
</style>