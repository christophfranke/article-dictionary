<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import type { PartialWord, ArticleDetail } from '../types';

import { useDictionaryView } from '@/use/dictionary';
import { useArticleView } from '@/use/articles';

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

import NotFoundView from '@/views/NotFoundView.vue';



const tableDisplayConfig = computed(() => ({
  header: true,
  limit: 0,
  sortBy: 'order',
  sortOrder: 'asc',
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

const displayFilter = (word: PartialWord): boolean => (
  wordIndexMap.value[word.original] > -1
  && (word.status === 'new' || word.status === 'seen')
);

const { dictionary } = useDictionaryView(displayFilter);

const highlighted = ref<{ word: string; index: number }>({
  word: '',
  index: -1,
});

const statusDescription = computed(() => {
  if (article.value?.status === 'read') {
    return 'You have read this article.';
  } else if (article.value?.status === 'seen') {
    return 'You have been reading this article.';
  } else {
    return 'New article';
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

const { fetchAuthorized: fetchAuthorizedButton, isLoading: isLoadingButton, errorMessage } = useApi();
const markArticleAsRead = async () => {
  const slug = article.value?.slug
  if (slug) {
    await articles.updateOne(slug, { status: 'read' });

    await new Promise(resolve => setTimeout(resolve, 100));
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
  dictionary.load();
  await articles.get(slug.value);

  if(article.value?.status === 'read') {
    timeoutId = setTimeout(() => {
      if (article.value) {
        articles.updateOne(article.value.slug, { status: 'seen' });
      }
    }, 60* SECOND);
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
    <Headline type="h2">Loading...</Headline>
  </div>
  <div class="article-page" v-else>
    <template v-if="article">
      <div :class="{ content: true, 'no-dictionary': !showDictionary }">
        <ArticleTopBar :article="article" :dictionary="dictionary" :statusDescription="statusDescription" />
        <Headline class="title">{{ article.title }}</Headline>
        <Paragraph>
          <ProcessedContent :words="article.words" :content="article.content" :dictionary="dictionary" v-model="highlighted" @click="toggleStatusSeen" :display="contentDisplayConfig" :scrollToIndex="article.readingIndex" />
        </Paragraph>
        <Tooltip :dictionary="dictionary" :highlighted="highlighted" :article="article" />
        <ArticleBottomBar :articleStatus="article.status" :isLoadingButton="isLoadingButton" :errorMessage="errorMessage" @markAsRead="markArticleAsRead" />
      </div>
      <DictionarySidebar :showDictionary="showDictionary" :dictionary="dictionary" :tableDisplayConfig="tableDisplayConfig" :highlightedWord="highlighted.word" :toggleShowDictionary="toggleShowDictionary" />
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
  margin-bottom: 20px;
}
</style>
