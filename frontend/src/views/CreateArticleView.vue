<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import useApi from '@/use/api';

import type { ArticleData, ArticleBase } from '@/types';

const article = ref<ArticleData>({
  title: '',
  content: '',
  privacy: 'public',
});

const router = useRouter();

const { fetchAuthorized, errorMessage, isLoading } = useApi();
const submitForm = async (): Promise<void> => {
  const data = await fetchAuthorized<ArticleBase>('/api/articles/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(article.value),
  });

  if (data) {
    router.push(`/articles/${data.slug}`);
  }
};
</script>

<template>
  <div class="create-article">
    <h1>Create Article</h1>
    <form @submit.prevent="submitForm" class="article-form">
      <label for="articleName">Title:</label>
      <input id="articleName" v-model="article.title" type="text" required />

      <label for="articleContent">Content:</label>
      <textarea id="articleContent" v-model="article.content" required></textarea>

      <label for="articlePrivacy">Privacy:</label>
      <select id="articlePrivacy" v-model="article.privacy">
        <option value="public">Public</option>
        <option value="private">Private</option>
      </select>

      <button type="submit" class="submit-button" :disabled="!isLoading">Submit</button>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.create-article {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #333;
  font-size: 2em;
  margin-bottom: 20px;
}

.article-form label {
  display: block;
  margin-bottom: 8px;
  color: #555;
}

.article-form input,
.article-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.article-form textarea {
  resize: vertical;
  min-height: 300px;
}

.article-form select {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  margin-top: 5px; /* Add margin for spacing */
}

.submit-button {
  margin-top: 20px;
  background-color: #28a745;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #218838;
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
