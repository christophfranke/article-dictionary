<template>
  <div>
    <h1>{{ article.title }}</h1>
    <div v-if="article.content && article.content.length">
      <h2>Content</h2>
      <p>
        <template v-for="(word, index) in article.content" :key="index">
          <span v-if="index > 0 && !punctuation.includes(word)">{{ ' ' }}</span>
          <span @click="toggleWord(word)" :class="{ selected: selectedWords.includes(word) }">
            {{ word }}
          </span>
        </template>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const article = ref({
  title: '',
  content: [], // Changed to an array of strings,
});

const punctuation = ['.', ',', '!', '?', ':', ';', '"', "'"];
const selectedWords = ref([]);

const route = useRoute();
const articleName = ref(route.params.name);

const fetchArticleDetails = async () => {
  try {
    const response = await fetch(`/api/articles/${articleName.value}`);
    if (response.ok) {
      article.value = await response.json();
    } else {
      console.error('Failed to fetch article details:', response.status);
      // Handle error as needed
    }
  } catch (error) {
    console.error('Error fetching article details:', error);
    // Handle error as needed
  }
};

const toggleWord = (word: string) => {
  if (selectedWords.value.includes(word)) {
    selectedWords.value = selectedWords.value.filter((w) => w !== word);
  } else {
    selectedWords.value.push(word);
  }
};

onMounted(() => {
  fetchArticleDetails();
});
</script>

<style scoped>
.selected {
  background-color: yellow;
  cursor: pointer;
}
</style>
