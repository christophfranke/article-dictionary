<script setup lang="ts">
import type { PropType } from 'vue';
import type { DictionaryView } from '@/dictionary/view';
import type { ArticleDetail } from '@/types';
import ButtonLink from '@/elements/ButtonLink.vue';
import Statistics from '@/components/Statistics.vue';
import __ from '@/i18n'

const props = defineProps({
  article: Object as PropType<ArticleDetail>,
  dictionary: Object as PropType<DictionaryView>,
  statusDescription: String,
});
</script>

<template>
  <div class="statistics-container" v-if="props.article && props.dictionary">
    <ButtonLink class="review" :to="`/articles/${props.article.slug}/review`">
      {{__('Review Words')}}
    </ButtonLink>
    <ButtonLink class="edit-article" :to="`/articles/${props.article.slug}/edit`">
      {{__('Edit Article')}}
    </ButtonLink>
    <Statistics :article="props.article" :dictionary="props.dictionary" showPercentage />
  </div>
  <p class="status-description">{{ props.statusDescription }}</p>
</template>

<style scoped>
.statistics-container {
  float: right;
  margin-left: 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.edit-article {
  margin-right: 20px;
}
.review {
  margin-right: 10px;
}

.status-description {
  margin-bottom: 40px;
  font-size: 14px;
}
</style>
