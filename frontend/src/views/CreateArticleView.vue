<template>
  <div>
    <h1>Create Article</h1>
    <form @submit.prevent="submitForm">
      <label for="articleName">Article Name:</label>
      <input id="articleName" v-model="article.name" type="text" required />

      <label for="articleContent">Article Content:</label>
      <textarea id="articleContent" v-model="article.content" required></textarea>

      <button type="submit">Submit</button>

      <p v-if="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

interface Article {
  name: string;
  content: string;
}

const article = ref<Article>({
  name: '',
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
