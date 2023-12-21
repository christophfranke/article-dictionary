<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
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

import Headline from '@/elements/Headline.vue';
import Button from '@/elements/Button.vue';
import ErroMessage from '@/elements/ErrorMessage.vue';
import Paragraph from '@/elements/Paragraph.vue';


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

const { articles } = useArticleView();
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
    if (!map[word]) {
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

const isLoading = computed<boolean>(() => !article.value?.title || dictionary.all.value.length === 0);

let timeoutId: ReturnType<typeof setTimeout> | null = null;
let SECOND = 1000;
onMounted(async () => {
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
  <div class="article-page" v-if="!article">
    <Headline type="h2">Loading...</Headline>
  </div>
  <div class="article-page" v-else>
    <div :class="{ content: true, 'no-dictionary': !showDictionary }">
      <Statistics :article="article" :dictionary="dictionary" showPercentage />
      <p class="status-description">{{ statusDescription }}</p>
      <Headline class="title">{{ article.title }}</Headline>
      <Paragraph>
        <ProcessedContent :words="article.words" :content="article.content" :dictionary="dictionary" v-model="highlighted" @click="toggleStatusSeen" :display="contentDisplayConfig" :scrollToIndex="article.readingIndex" />
      </Paragraph>
      <Button
        v-if="article.status !== 'read'"
        :disabled="isLoadingButton"
        class="mark-as-read"
        @click="markArticleAsRead"
      >Mark as read</Button>
      <ErroMessage :message="errorMessage" />
    </div>
    <div class="dictionary-container" :class="{ hidden: !showDictionary}">
      <Button class="toggle-dictionary-button" @click="toggleShowDictionary" role="view">
        <FontAwesomeIcon icon="chevron-right" :class="{ rotate: !showDictionary}" />
      </Button>
      <div class="dictionary-scoller">
        <DictionaryTable :dictionary="dictionary" :display="tableDisplayConfig" sort="number" :highlight="highlighted.word" />
      </div>
    </div>
    <Tooltip :dictionary="dictionary" :highlighted="highlighted" :article="article" />
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
  background-color: $background-100;
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
