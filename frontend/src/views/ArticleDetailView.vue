<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import type { Word, ArticleDetail } from '../types';

import { useCustomDictionary } from '@/use/dictionary';
import useApi from '@/use/api';
import { useToggleStatusSeen } from '@/use/toggle-status-seen';

import DictionaryTable from '@/components/DictionaryTable.vue';
import Statistics from '@/components/Statistics.vue';
import Tooltip from '@/components/Tooltip.vue';
import ProcessedContent from '@/components/ProcessedContent.vue';

import Headline from '@/elements/Headline.vue';
import Button from '@/elements/Button.vue';
import ErroMessage from '@/elements/ErrorMessage.vue';


const tableDisplayConfig = computed(() => ({
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
    known: false,
    ignore: true,
    add: false,
    sort: true,
    edit: true,
    retranslate: true,
    status: false,
    glosbe: true,
    detail: false,
    link: true,
  },
  behaviour: {
    highlight: showDictionary.value,
    scroll: showDictionary.value,
  }
}));

const contentDisplayConfig = {
  highlight: {
    new: true,
    seen: true,
    mark: false,
  }  
}

const article = ref<ArticleDetail>({
  id: '',
  title: '',
  content: '',
  slug: '',
  status: '',
  owned: false,
  privacy: '',
  words: [],
  dictionary: [],
});

const route = useRoute();
const { fetchAuthorized, errorMessage, isLoading } = useApi();

const displayFilter = (word: Word): boolean => word.status === 'new' || word.status === 'seen';
const dictionary = useCustomDictionary([], displayFilter);

const highlightedWord = ref<string>('');
const newWordsCount = computed<number>(() => dictionary.words.value.filter((word) => word.status === 'new').length);


const statusDescription = computed(() => {
  if (article.value.status === 'read') {
    return 'You have read this article.';
  } else if (article.value.status === 'seen') {
    return 'You have been reading this article.';
  } else {
    return 'New article';
  }

})

const markArticleAsSeen = async () => {
  const result = await fetchAuthorized('/api/articles/seen', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: article.value.id }),
  });
  
  if (result) {
    article.value.status = 'seen';
  }
}

const fetchArticleDetails = async () => {
  const slug = route.params.slug;
  if (!slug) {
    console.error('No slug provided');
    return;
  }
  const data = await fetchAuthorized<ArticleDetail>(`/api/articles/${slug}`);
  if (data) {
    article.value = data;

    // Sort dictionary based on position in article
    const lowerCaseWords = article.value.words.map((word) => word.toLowerCase());
    article.value.dictionary.sort(
      (a, b) => lowerCaseWords.indexOf(a.original) - lowerCaseWords.indexOf(b.original)
    );
    
    dictionary.set(article.value.dictionary)
  } else {
    console.error('Failed to fetch article details');
  }
};

// this function is currently unused, but may be useful in the future
const markAllAsSeen = async () => {
  const words = dictionary.words.value.filter((word) => word.status === 'new');
  if (words.length > 0) {
    await dictionary.updateMany(words.map((word) => word.original), { status: 'seen' });
  }
};

const markArticleAsRead = async () => {
  const data = await fetchAuthorized<ArticleDetail>(`/api/articles/${article.value.slug}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: 'read' }),
  });

  if (data) {
    article.value = data;
  }
}

const showDictionary = ref(true);
const toggleShowDictionary = () => {
  showDictionary.value = !showDictionary.value;
};

const toggleStatusSeen = useToggleStatusSeen(dictionary)


let timeoutId: ReturnType<typeof setTimeout> | null = null
const SECOND: number = 1000
const TIME_TO_MARK_AS_SEEN: number = 60 * SECOND;
onMounted(() => {
  fetchArticleDetails();

  timeoutId = setTimeout(() => {
    markArticleAsSeen();
  }, TIME_TO_MARK_AS_SEEN);
});

onBeforeUnmount(() => {
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
});

</script>


<template>
  <div class="article-page" v-if="article.title">
    <div :class="{ content: true, 'no-dictionary': !showDictionary }" v-if="article.content && article.content.length">
      <Statistics :article="article" :dictionary="dictionary" showPercentage />
      <p class="status-description">{{ statusDescription }}</p>
      <Headline class="title">{{ article.title }}</Headline>
      <ProcessedContent :words="article.words" :content="article.content" :dictionary="dictionary" v-model="highlightedWord" @click="toggleStatusSeen" :display="contentDisplayConfig" />
      <Button
        v-if="article.status !== 'read'"
        :disabled="isLoading"
        class="mark-as-read"
        @click="markArticleAsRead"
      >Mark as read</Button>
      <ErroMessage :message="errorMessage" />
    </div>
    <div class="dictionary-container" :class="{ hidden: !showDictionary}">
      <Button class="toggle-dictionary-button" @click="toggleShowDictionary">
        <FontAwesomeIcon icon="chevron-right" :class="{ rotate: !showDictionary}" />
      </Button>
      <div class="dictionary-scoller">
        <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" sort="number" :highlight="highlightedWord" />
      </div>
    </div>
    <Tooltip :dictionary="dictionary" :highlightedWord="highlightedWord" v-model="highlightedWord" />
  </div>
</template>

<style scoped lang="scss">
.article-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.content {
  max-width: 800px;
  width: calc(10px + 50vw);
  margin-right: 20px;

  &.no-dictionary {
    max-width: 1000px;
    margin: 0 auto;
    width: 100vw;
  }
}

@media (max-width: 1240px) {
  .content {
    width: calc(100vw - 610px);
    &.no-dictionary {
      margin: 0 auto;
      width: calc(100vw - 70px);
    }
  }
}

@media (max-width: 1000px) {
  .content {
    width: calc(100vw - 40px);
  }
}

.status-description {
  margin-bottom: 40px;
  font-size: 14px;
}

.title {
  margin-bottom: 20px;
}

.mark-as-read {
  margin-top: 30px;
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

  svg {
    transition: transform 0.3s ease;
  }
  .rotate {
    transform: rotate(180deg);
  }
}


.statistics {
  float: right;
  margin-left: 20px;
}
</style>
