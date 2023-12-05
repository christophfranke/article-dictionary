<template>
  <div>
    <DictionaryTable :words="displayedWords" :updateWords="updateWords" :display="tableDisplayConfig" />
    <h1>{{ article.title }}</h1>
    <div v-if="article.content && article.content.length">
      <p>
        <template v-for="({ word, separator }, index) in processedContent" :key="index">
          <span>{{ separator }}</span>
          <span @click="toggleWord(word)" :class="{ selected: selectedWords.includes(word.toLowerCase()) }">
            {{ word }}
          </span>
        </template>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import DictionaryTable from '../components/DictionaryTable.vue';

interface Word {
  index: number;
  original: string;
  translations: string[];
  status: string;
}

interface Article {
  title: string;
  content: string;
  words: string[];
  dictionary: Word[]
}

interface ProcessedContentItem {
  word: string;
  separator: string;
}

const tableDisplayConfig = {
  header: true,
  col: {
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
  }
};


const article = ref<Article>({
  title: '',
  content: '',
  words: [],
  dictionary: [],
});

const selectedWords = ref<string[]>([]);
const displayedWords = computed<Word[]>(() => {
  return article.value.dictionary
    .filter((word) => selectedWords.value.includes(word.original.toLowerCase()))
    .map((word, index) => ({ ...word, index }));
});

const updateWords = (newWords: Word[]): void => {
  article.value.dictionary = newWords;
};


const route = useRoute();
const articleName = ref<string>(route.params.name ? String(route.params.name) : '');

const fetchArticleDetails = async () => {
  try {
    const response = await fetch(`/api/articles/${articleName.value}`);
    if (response.ok) {
      article.value = await response.json();
      // Initialize selectedWords with words from the dictionary with status new or seen
      selectedWords.value = article.value.dictionary
        .filter(word => word.status === 'new' || word.status === 'seen')
        .map(word => word.original.toLowerCase());
    } else {
      console.error('Failed to fetch article details:', response.status);
      // Handle error as needed
    }
  } catch (error) {
    console.error('Error fetching article details:', error);
    // Handle error as needed
  }
};

const toggleWord = (word: string): void => {
  if (selectedWords.value.includes(word)) {
    selectedWords.value = selectedWords.value.filter((w) => w !== word);
  } else {
    selectedWords.value.push(word);
  }
};

const getSeparator = (index: number, nextWord: string): string => {
  const nextIndex = article.value.content.substring(index).indexOf(nextWord);
  return nextIndex === -1 || nextIndex === 0
    ? ''
    : article.value.content.substring(index, index + nextIndex);
};

const processedContent = computed<ProcessedContentItem[]>(() => {
  const result: ProcessedContentItem[] = [];
  let currentIndex = 0;

  article.value.words.forEach((word, index) => {
    const separator = getSeparator(currentIndex, word);
    result.push({ word, separator });
    currentIndex += separator.length + word.length;
  });

  return result;
});

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
