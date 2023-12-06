<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import type { PartialArticle } from '../types';

const article = ref<PartialArticle>({
  title: '',
  content: '',
});

const error = ref<string>('');
const router = useRouter();

const submitForm = async (): Promise<void> => {
  try {
    const response = await fetch('/api/articles/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(article.value),
    });

    const responseData = await response.json();

    if (response.ok) {
      // If there's a 'url' field in the response, redirect to that URL
      if (responseData.url) {
        router.push(responseData.url);
      } else {
        console.error('Invalid response format: missing "url" field.');
        // Handle error as needed
      }
    } else {
      // If there's an 'error' field in the response, display the error
      if (responseData.error) {
        error.value = responseData.error;
      } else {
        console.error('Invalid response format: missing "error" field.');
        // Handle error as needed
      }
    }
  } catch (error) {
    console.error('Error creating article:', error);
    // Handle error as needed
  }
};
</script>

<template>
  <div class="create-article">
    <h1>Create Article</h1>
    <form @submit.prevent="submitForm" class="article-form">
      <label for="articleName">Article Name:</label>
      <input id="articleName" v-model="article.title" type="text" required />

      <label for="articleContent">Article Content:</label>
      <textarea id="articleContent" v-model="article.content" required></textarea>

      <button type="submit" class="submit-button">Submit</button>

      <p v-if="error" class="error-message">{{ error }}</p>
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

.submit-button {
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
