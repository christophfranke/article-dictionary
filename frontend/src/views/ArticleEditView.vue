<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useArticleView } from '@/use/articles';

import type { ArticleData, ArticleBase } from '@/types';

import Headline from '@/elements/Headline.vue';
import Form from '@/elements/Form.vue';
import FormGroup from '@/elements/FormGroup.vue';
import Label from '@/elements/Label.vue';
import Button from '@/elements/Button.vue';
import Input from '@/elements/Input.vue';
import Select from '@/elements/Select.vue';
import Textarea from '@/elements/Textarea.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';


const article = ref<ArticleBase | null>(null);

const route = useRoute();
const slug = ref<string>(typeof route.params.slug === 'string' ? route.params.slug : (route.params.slug[0] || ''));

const router = useRouter();

const { articles, errorMessage, isLoading } = useArticleView();
const submitForm = async (): Promise<void> => {
  if (article.value) {    
    const updatedArticle = await articles.updateOne(slug.value, article.value)

    if (updatedArticle) {
      router.push(`/articles/${updatedArticle.slug}`);
    }
  }
};

onMounted(async () => {
  article.value = articles.detail(slug.value).value || await articles.get(slug.value);
  console.log(article.value);

  if (!article.value) {
    router.push('/404-not-found');
  }
});
</script>

<template>
  <div class="create-article" v-if="article">
    <Headline>Edit Article</Headline>
    <Form @submit.prevent="submitForm" class="article-form">
      <Label for="articleName">Title:</Label>
      <Input id="articleName" v-model="article.title" type="text" required :disabled="isLoading" />

      <Label for="articleContent">Content:</Label>
      <Textarea id="articleContent" v-model="article.content" required :disabled="isLoading" />

      <Label for="articlePrivacy">Privacy:</Label>
      <Select id="articlePrivacy" v-model="article.privacy" :disabled="isLoading">
        <option value="public">Public</option>
        <option value="private">Private</option>
      </Select>

      <Button type="submit" class="submit-button" :disabled="isLoading">Submit</Button>

      <ErrorMessage class="error" :message="errorMessage" />
    </form>
  </div>
</template>

<style scoped>
.create-article {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.article-form label {
  margin-bottom: 8px;
}

.article-form input,
.article-form textarea {
  margin-bottom: 15px;
}

.article-form select {
  margin-top: 5px;
}

.submit-button {
  margin-top: 20px;
}

.error {
  margin-top: 20px;
}
</style>
