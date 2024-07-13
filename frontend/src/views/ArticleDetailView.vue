<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import type { PartialWord, ArticleDetail } from '../types';

import { useDictionaryView } from '@/use/dictionary';
import { useArticleView } from '@/use/articles';

import usePagination from '@/components/ArticleDetailView/use-pagination';

import useApi from '@/use/api';
import { useToggleStatusSeen } from '@/use/toggle-status-seen';

import DictionaryTable from '@/components/DictionaryTable.vue';
import Statistics from '@/components/Statistics.vue';
import Tooltip from '@/components/Tooltip.vue';
import ProcessedContent from '@/components/ProcessedContent.vue';

import ArticleTopBar from '@/components/ArticleDetailView/TopBar.vue';
import ArticleBottomBar from '@/components/ArticleDetailView/BottomBar.vue';
import DictionarySidebar from '@/components/ArticleDetailView/DictionarySidebar.vue';

import Headline from '@/elements/Headline.vue';
import Button from '@/elements/Button.vue';
import ButtonLink from '@/elements/ButtonLink.vue';
import ErroMessage from '@/elements/ErrorMessage.vue';
import Paragraph from '@/elements/Paragraph.vue';
import Pagination from '@/elements/Pagination.vue';

import NotFoundView from '@/views/NotFoundView.vue';
import __ from '@/i18n'


const contentDisplayConfig = {
  padding: true,
  click: true,
  highlight: {
    new: true,
    seen: true,
    mark: false,
  }  
}

const route = useRoute();
const slug = ref(typeof route.params.slug === 'string' ? route.params.slug : (route.params.slug[0] || ''));

const { articles, isLoading } = useArticleView();
const article = articles.detail(slug.value)

const {
  currentPage,
  numberOfPages,
  paginatedContent,
  paginatedWords,
  relativeIndex,
  getAbsoluteIndex,
} = usePagination(article);

watch(() => article.value?.content, () => {
  if (relativeIndex.value.page > 0) {
    currentPage.value = relativeIndex.value.page  
  }
}, { immediate: true });


const displayFilter = (word: PartialWord): boolean => (
  wordIndexMap.value[word.original] > -1
  && (word.status === 'new' || word.status === 'seen')
  && paginatedWords.value.includes(word.original)
);

const { dictionary } = useDictionaryView(displayFilter);

const highlighted = ref<{ word: string; index: number }>({
  word: '',
  index: -1,
});
const absoluteHighlighted = computed(() => ({
  ...highlighted.value,
  index: getAbsoluteIndex(highlighted.value?.index ?? -1),
}));

const statusDescription = computed(() => {
  if (article.value?.status === 'read') {
    return __('You have read this article.');
  } else if (article.value?.status === 'seen') {
    return __('You have been reading this article.');
  } else {
    return __('New article');
  }

  return ''
})

const wordIndexMap = computed(() => {
  const map: { [key: string]: number } = {};
  article.value?.words.forEach((word, index) => {
    if (!(word in map)) {
      map[word] = index;
    }
  });

  return map;
});
dictionary.setOrder((word: PartialWord) => wordIndexMap.value[word.original] ?? Infinity);

const { fetchAuthorized: fetchAuthorizedButton, errorMessage } = useApi();

const scrollToTop = async () => {
  await new Promise(resolve => setTimeout(resolve, 50));
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

const isLoadingButton = ref<boolean>(false)
const markArticleAsRead = async () => {
  isLoadingButton.value = true
  const slug = article.value?.slug
  if (slug) {
    await articles.updateOne(slug, { status: 'read' });

    currentPage.value = 1;
  }

  isLoadingButton.value = false
}
const changePage = async () => {
  await scrollToTop();
  if (article.value) {
    await articles.updateOne(article.value.slug, { readingIndex: getAbsoluteIndex(0) });
  }
}

const showDictionary = ref(true);
const toggleShowDictionary = () => {
  showDictionary.value = !showDictionary.value;
};

const toggleStatusSeen = useToggleStatusSeen(dictionary)
const router = useRouter();

let timeoutId: ReturnType<typeof setTimeout> | null = null;
let SECOND = 1000;
onMounted(async () => {
  await articles.get(slug.value)
  dictionary.load()

  if(article.value?.status === 'read') {
    timeoutId = setTimeout(() => {
      if (article.value) {
        articles.updateOne(article.value.slug, { status: 'seen' });
      }
    }, 60 * SECOND);
  }
});

onBeforeUnmount(() => {
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
});


</script>


<template>
  <div class="article-page" v-if="!article && isLoading">
    <Headline type="h2">{{ __('Loading...') }}</Headline>
  </div>
  <div class="article-page" v-else>
    <template v-if="article">
      <div :class="{ content: true, 'no-dictionary': !showDictionary }">
        <ArticleTopBar :article="article" :dictionary="dictionary" :statusDescription="statusDescription" />
        <Headline class="title" v-if="currentPage === 1">{{ article.title }}</Headline>
        <Headline type="h3" class="title" v-else>{{ article.title }} ({{ currentPage }}/{{ numberOfPages }})</Headline>
        <Paragraph>
          <ProcessedContent :words="paginatedWords" :content="paginatedContent" :dictionary="dictionary" v-model="highlighted" @click="toggleStatusSeen" :display="contentDisplayConfig" :scrollToIndex="relativeIndex.page === currentPage ? relativeIndex.index : 0" :key="currentPage" />
        </Paragraph>
        <ArticleBottomBar :articleStatus="article.status" :isLoadingButton="isLoadingButton" :errorMessage="errorMessage" @markAsRead="markArticleAsRead" v-if="currentPage === numberOfPages" />
        <Pagination 
          class="bottom-pagination"
          v-model:currentPage="currentPage" 
          :numberOfPages="numberOfPages"
          v-if="numberOfPages > 1"
          @change="changePage"
        />
        <Tooltip :dictionary="dictionary" :highlighted="absoluteHighlighted" :article="article" />
      </div>
      <DictionarySidebar :showDictionary="showDictionary" :dictionary="dictionary" :highlightedWord="highlighted.word" :toggleShowDictionary="toggleShowDictionary" />
    </template>
    <NotFoundView v-else />
  </div>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

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

.title {
  clear: both;
  margin-bottom: 50px;
}

.bottom-pagination {
  margin-top: 50px;
}
</style>
