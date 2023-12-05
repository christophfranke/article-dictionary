<template>
  <div>
    <router-link :to="data.url">
      <h2>{{ data.title }}</h2>
      <p>{{ data.excerpt }}...</p>
    </router-link>
  </div>
</template>

<script setup lang="ts">
interface ArticleProps {
  data: {
    url: string;
    title: string;
    excerpt: string;
    // Add other properties as needed
  };
}

const props = defineProps<ArticleProps>();
</script>
