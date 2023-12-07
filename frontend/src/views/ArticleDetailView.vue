<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

import type { Word, ArticleDetail } from '../types';

import createDictionaryCollection from '../dictionary/collection';

import DictionaryTable from '../components/DictionaryTable.vue';
import Statistics from '../components/Statistics.vue';
import Tooltip from '../components/Tooltip.vue';
import ArticleContent from '../components/ArticleContent.vue';


const tableDisplayConfig = {
  header: true,
  col: {
    number: true,
    original: true,
    translations: true,
    status: false,
    actions: true,
  },
  action: {
    known: true,
    ignore: true,
    add: false,
    sort: true,
    edit: true,
    retranslate: true,
    status: false,
  },
};

const article = ref<ArticleDetail>({
  id: '',
  title: '',
  content: '',
  slug: '',
  words: [],
  dictionary: [],
});

const highlightedWord = ref<string>('');

const route = useRoute();
const articleName = ref<string>(route.params.name ? String(route.params.name) : '');

const displayedWords = computed<Word[]>(() => dictionary.get());
const newWordsCount = computed<number>(() => dictionary.get().filter((word) => word.status === 'new').length);

const displayFilter = (word: Word): boolean => word.status === 'new' || word.status === 'seen';
const dictionary = createDictionaryCollection([], displayFilter);

const fetchArticleDetails = async () => {
  try {
    const response = await fetch(`/api/articles/${articleName.value}`);
    if (response.ok) {
      article.value = await response.json();

      // Sort dictionary based on occurrences in article content
      article.value.dictionary.sort((a, b) => {
        const indexA = getWordIndex(a.original);
        const indexB = getWordIndex(b.original);

        if (indexA < indexB) {
          return -1;
        }
        if (indexA > indexB) {
          return 1;
        }
        // If indices are equal, sort by original order
        if (a.index < b.index) {
          return -1;
        }
        if (a.index > b.index) {
          return 1;
        }
        return 0;
      });

      // Function to get the index of the word in content, considering word boundaries
      function getWordIndex(word: string) {
        const regex = new RegExp(`${word}`, 'i');
        const index = article.value.content.search(regex);
        return index >= 0 ? index : Infinity;
      }
      
      dictionary.set(article.value.dictionary)
    } else {
      console.error('Failed to fetch article details:', response.status);
      // Handle error as needed
    }
  } catch (error) {
    console.error('Error fetching article details:', error);
    // Handle error as needed
  }
};

const markAllAsSeen = () => {
  const words = dictionary.get().filter((word) => word.status === 'new');
  dictionary.updateMany(words.map((word) => word.original), { status: 'seen' });
};


onMounted(() => {
  fetchArticleDetails();
});
</script>

<template>
  <div class="article-page" v-if="article.title">
    <div class="content">
      <div v-if="article.content && article.content.length">
        <ArticleContent :words="article.words" :content="article.content" :dictionary="dictionary" v-model="highlightedWord" />
      </div>
    </div>
    <div class="dictionary-container">
      <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" sort="number" :highlight="highlightedWord" />
    </div>
    <Tooltip :dictionary="dictionary" :highlightedWord="highlightedWord" v-model="highlightedWord" />
  </div>
</template>

<style scoped>
.article-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.content {
  max-width: 800px;
  width: calc(100vw - 600px);
  margin-right: 20px;
}

h1 {
  color: #333;
  font-size: 2em;
  margin-bottom: 20px;
}

.dictionary-container {
  background-color: white;
  position: fixed;
  top: 20px; /* Adjust the top position as needed */
  right: 20px; /* Adjust the right position as needed */
  max-height: calc(100vh - 40px); /* Set a minimum height for the dictionary container */
  max-width: 500px;
  padding-bottom: 20px;
  overflow-y: auto; /* Enable vertical scroll for the dictionary */
}

.mark-all-seen-button {
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50; /* Green background */
  color: white; /* White text */
  border: none; /* Remove borders */
  border-radius: 5px; /* Rounded corners */
  cursor: pointer; /* Add a pointer cursor on hover */
}

/* Add a hover effect */
.mark-all-seen-button:hover {
  background-color: #45a049;
}

.mark-all-seen-button:disabled {
  background-color: #b0b0b0; /* Light gray background for disabled state */
  cursor: default; /* Default cursor on disabled state */
  color: #666; /* Dim text color for disabled state */
}

.statistics {
  float: right;
}
</style>
