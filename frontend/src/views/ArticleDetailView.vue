<template>
  <div>
    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>

    <!-- Display the dictionary button -->
    <button @click="showDictionary">Show Dictionary</button>

    <!-- Display the dictionary content when the button is clicked -->
    <div v-if="showDictionaryContent">
      <h2>Dictionary</h2>
      <ul>
        <li v-for="(value, key) in article.dictionary" :key="key">
          {{ key }}: {{ value }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const article = ref({
  title: '',
  content: '',
  dictionary: {}, // Placeholder for the dictionary data
});

const showDictionaryContent = ref(false);

// Access the dynamic route parameter (article name)
const route = useRoute();
const articleName = ref(route.params.name);

// Fetch article details from the server
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

// Function to toggle the visibility of the dictionary content
const showDictionary = () => {
  showDictionaryContent.value = !showDictionaryContent.value;
};

// Fetch article details when the component is mounted
onMounted(() => {
  fetchArticleDetails();
});
</script>
