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
        console.log(word, index, regex)
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
    </div>
    <div class="dictionary-container">
      <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" sort="number" :highlight="highlightedWord" />
    </div>
  </div>
</template>

<style scoped>
.article-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.content {
  flex: 2; /* Increase the size of the article content */
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
  flex: 1; /* Decrease the size of the dictionary */
}
</style>
