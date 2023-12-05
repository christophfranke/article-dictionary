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

<template>
  <div class="article-preview">
    <router-link :to="data.url">
      <h2>{{ data.title }}</h2>
      <p>{{ data.excerpt }}...</p>
    </router-link>
  </div>
</template>

<style scoped>
.article-preview {
  background-color: #fff; /* Bright background color */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.article-preview:hover {
  transform: translateY(-5px);
}

h2 {
  color: #333; /* Dark font color */
  margin-bottom: 10px;
}

p {
  color: #666; /* Slightly darker text color */
  margin: 0;
}
</style>
