<template>
  <div>
    <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" />
    <h1>{{ article.title }}</h1>
    <div v-if="article.content && article.content.length">
      <p>
        <template v-for="({ word, separator }, index) in processedContent" :key="index">
          <span>{{ separator }}</span>
          <br v-if="separator === '\n'" />
          <br v-if="separator === '\n\n'" />
          <br v-if="separator === '\n\n'" />
          <span @click="toggleStatusSeen(word)" :class="{ selected: displayedWords.some(entry => entry.original === word.toLowerCase()) }">
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
import createDictionaryCollection from '../services/dictionary-collection';

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
  dictionary: Word[];
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
  },
};

const article = ref<Article>({
  title: '',
  content: '',
  words: [],
  dictionary: [],
});


const route = useRoute();
const articleName = ref<string>(route.params.name ? String(route.params.name) : '');

const displayedWords = computed<Word[]>(() => dictionary.get());

const displayFilter = word => word.status === 'new' || word.status === 'seen'
const dictionary = createDictionaryCollection([], displayFilter);

const fetchArticleDetails = async () => {
  try {
    const response = await fetch(`/api/articles/${articleName.value}`);
    if (response.ok) {
      article.value = await response.json();
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

const toggleStatusSeen = (word: string) => {
  const original = word.toLowerCase()
  dictionary.updateWord(original, { status: ['new', 'seen'].includes(dictionary.find(original)?.status) ? 'known' : 'seen' });
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
