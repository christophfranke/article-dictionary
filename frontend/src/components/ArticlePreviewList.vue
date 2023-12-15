<script setup lang="ts">
import type { ArticlePreview } from '@/types';
import ArticlePreviewComponent from '@/components/ArticlePreview.vue';

import Headline from '@/elements/Headline.vue';
import ButtonLink from '@/elements/ButtonLink.vue';


const props = defineProps({
  title: {
    type: String,
    required: true
  },
  articleList: {
    type: Array as unknown as () => ArticlePreview[],
    required: true,
  },
  showCreateButton: {
    type: Boolean,
    default: true
  }
})
</script>

<template>
  <template v-if="props.articleList.length > 0">
    <Headline type="h2" class="title">{{ props.title }}</Headline>
    <div class="article-list">
      <ArticlePreviewComponent v-for="article in props.articleList" :key="article.id" :article="article" />
    </div>

    <ButtonLink v-if="props.showCreateButton" to="/create" class="create-link">Create New Article</ButtonLink>
  </template>
</template>

<style scoped>
.article-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.title {
  margin-bottom: 20px;
}

.create-link {
  display: block;
  margin: 20px auto;
}
</style>