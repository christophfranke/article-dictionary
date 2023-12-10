<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import type { Word, ArticleDetail } from '../types';

import useDictionary from '@/use/dictionary';
import { useFetchAuthorized } from '@/use/api';

import DictionaryTable from '../components/DictionaryTable.vue';
import Statistics from '../components/Statistics.vue';
import Tooltip from '../components/Tooltip.vue';
import ArticleContent from '../components/ArticleContent.vue';



const tableDisplayConfig = {
  header: true,
  limit: 0,
  col: {
    number: true,
    original: true,
    translations: true,
    status: false,
    actions: true,
    frequency: false,
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

const newWordsCount = computed<number>(() => dictionary.words.value.filter((word) => word.status === 'new').length);

const displayFilter = (word: Word): boolean => word.status === 'new' || word.status === 'seen';
const dictionary = useDictionary([], displayFilter);

const fetchAuthorized = useFetchAuthorized();

const fetchArticleDetails = async () => {
  const data = await fetchAuthorized<ArticleDetail>(`/api/articles/${articleName.value}`);
  if (data) {
    article.value = data;

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

    await fetchAuthorized('/api/articles/seen', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: article.value.id }),
    });
  } else {
    console.error('Failed to fetch article details');
    // Handle error as needed
  }
};

const markAllAsSeen = () => {
  const words = dictionary.words.value.filter((word) => word.status === 'new');
  dictionary.updateMany(words.map((word) => word.original), { status: 'seen' });
};

const showDictionary = ref(true);
const toggleShowDictionary = () => {
  showDictionary.value = !showDictionary.value;
};


onMounted(() => {
  fetchArticleDetails();
});
</script>

<template>
  <div class="article-page" v-if="article.title">
    <div :class="{ content: true, 'no-dictionary': !showDictionary }" v-if="article.content && article.content.length">
      <Statistics :article="article" :dictionary="dictionary" showPercentage />
      <h1>{{ article.title }}</h1>
      <ArticleContent :words="article.words" :content="article.content" :dictionary="dictionary" v-model="highlightedWord" />
      <button :disabled="newWordsCount === 0" class="mark-all-seen-button" @click="markAllAsSeen">Mark All as Seen</button>
    </div>
    <div class="dictionary-container" :class="{ hidden: !showDictionary}">
      <button class="toggle-dictionary-button" @click="toggleShowDictionary">
        <FontAwesomeIcon icon="chevron-right" :class="{ rotate: !showDictionary}" />
      </button>
      <div class="dictionary-scoller">
        <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" sort="number" :highlight="highlightedWord" />
      </div>
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
  width: calc(10px + 50vw);
  margin-right: 20px;
}

.content.no-dictionary {
  max-width: 1000px;
  margin: 0 auto;
  width: 100vw;
}

@media (max-width: 1240px) {
  .content {
    width: calc(100vw - 610px);
  }

  .content.no-dictionary {
    margin: 0 auto;
    width: calc(100vw - 70px);
  }
}

@media (max-width: 1000px) {
  .content {
    width: calc(100vw - 40px);
  }
}


h1 {
  color: #333;
  font-size: 2em;
  margin-bottom: 20px;
}

.dictionary-container {
  background-color: white;
  position: fixed;
  top: 20px;
  right: 20px;
  max-height: calc(100vh - 40px);
  max-width: 550px;
  padding-bottom: 20px;
  /* do not clip horizontal overflow */
  overflow-x: visible;

  transition: transform 0.3s ease;
}

.dictionary-container.hidden {
  transform: translateX(100%); /* Slide out to the right when hidden */
}

.dictionary-scoller {
  max-height: calc(100vh - 40px);
  overflow-y: auto; /* Enable vertical scroll for the dictionary */
}

.toggle-dictionary-button {
  position: absolute;
  top: 0;
  left: -10px;
  transform: translateX(-100%);
  padding: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.toggle-dictionary-button:hover {
  background-color: #2980b9;
}

.toggle-dictionary-button svg {
  transition: transform 0.3s ease;
}

.rotate {
  transform: rotate(180deg);
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
  margin-left: 20px;
}
</style>
