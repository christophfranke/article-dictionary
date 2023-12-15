<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import useApi from '@/use/api';

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


const article = ref<ArticleData>({
  title: '',
  content: '',
  privacy: 'public',
});

const router = useRouter();

const { fetchAuthorized, errorMessage, isLoading } = useApi();
const submitForm = async (): Promise<void> => {
  const data = await fetchAuthorized<ArticleBase>('/api/articles/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(article.value),
  });

  if (data) {
    router.push(`/articles/${data.slug}`);
  }
};
</script>

<template>
  <div class="create-article">
    <Headline>Create Article</Headline>
    <Form @submit.prevent="submitForm" class="article-form">
      <Label for="articleName">Title:</Label>
      <Input id="articleName" v-model="article.title" type="text" required />

      <Label for="articleContent">Content:</Label>
      <Textarea id="articleContent" v-model="article.content" required />

      <Label for="articlePrivacy">Privacy:</Label>
      <Select id="articlePrivacy" v-model="article.privacy">
        <option value="public">Public</option>
        <option value="private">Private</option>
      </Select>

      <Button type="submit" class="submit-button" :disabled="isLoading">Submit</Button>

      <ErrorMessage :message="errorMessage" />
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
</style>
