<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import DictionaryTable from '../components/DictionaryTable.vue';
import createDictionaryCollection from '../services/dictionary-collection';

interface Word {
  id: string;
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

const article = ref<Article>({
  title: '',
  content: '',
  words: [],
  dictionary: [],
});

const highlightedWord = ref<string>('');
const setHighlight = (word: string) => {
  highlightedWord.value = word;
};
const unsetHighlight = (word: string) => {
  if (highlightedWord.value === word) {
    highlightedWord.value = '';
  }
};



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
      function getWordIndex(word) {
        const regex = new RegExp(`${word}`, 'i');
        const index = article.value.content.search(regex);
        return index >= 0 ? index : Math.Infinity;
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
  dictionary.updateWord(original, { status: ['new', 'seen'].includes(dictionary.find(original)?.status || '') ? 'known' : 'seen' });
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
  <div class="article-page">
    <div class="content">
      <h1>{{ article.title }}</h1>
      <div v-if="article.content && article.content.length">
        <p>
          <template v-for="({ word, separator }, index) in processedContent" :key="index">
            <span class="separator">{{ separator }}</span>
            <br v-if="separator === '\n'" />
            <br v-if="separator === '\n\n'" />
            <br v-if="separator === '\n\n'" />
            <span
              @mouseover="setHighlight(word)"
              @mouseout="unsetHighlight(word)"
              @click="toggleStatusSeen(word)"
              :class="{ new: displayedWords.find(entry => entry.original === word.toLowerCase())?.status === 'new', seen: displayedWords.find(entry => entry.original === word.toLowerCase())?.status === 'seen' }"
            >
              {{ word }}
            </span>
          </template>
        </p>
      </div>
      <button :disabled="newWordsCount === 0" class="mark-all-seen-button" @click="markAllAsSeen">Mark All as Seen</button>
    </div>
    <div class="dictionary-container">
      <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" sort="number" :highlight="highlightedWord" />
    </div>
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

p {
  font-size: 18px;
  line-height: 2;
}

span {
  cursor: pointer;
  padding: 2px 3px;
}

span.separator {
  padding: 2px 0;
  margin: 0 -2px;
}

span.new {
  background-color: rgba(51, 153, 255, 0.15);
}

span.seen {
  background-color: rgba(0, 153, 51, 0.15);
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
</style>
