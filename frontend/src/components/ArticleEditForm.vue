<!-- ArticleEditForm.vue -->
<script setup lang="ts">
import type { PropType } from 'vue';
import type { ArticleData } from '@/types';

import Input from '@/elements/Input.vue';
import Select from '@/elements/Select.vue';
import Textarea from '@/elements/Textarea.vue';
import Button from '@/elements/Button.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';
import Label from '@/elements/Label.vue';
import Form from '@/elements/Form.vue';


const MAX_LENGTH = 50000;


const props = defineProps({
  article: Object as PropType<ArticleData>,
  isLoading: Boolean,
  errorMessage: String as PropType<String | null>
});

const emit = defineEmits(['submit']);

const onSubmit = () => {
  emit('submit');
};
</script>

<template>
  <Form @submit.prevent="onSubmit" class="article-form" v-if="article">
    <Label for="articleName" class="title">Title:</Label>
    <Input id="articleName" v-model="article.title" type="text" required :disabled="isLoading" />

    <Label for="articleContent">Content:</Label>
    <Textarea id="articleContent" v-model="article.content" required :disabled="isLoading" :max-length="MAX_LENGTH" />
    <span class="char-count">
      {{ article.content.length }}/{{ MAX_LENGTH || '∞' }}
    </span>      

    <Label for="articlePrivacy">Privacy:</Label>
    <Select id="articlePrivacy" v-model="article.privacy" :disabled="isLoading">
      <option value="public">Public</option>
      <option value="private">Private</option>
    </Select>

    <Button type="submit" class="submit-button" :disabled="isLoading">Submit</Button>

    <ErrorMessage class="error" :message="errorMessage" v-if="errorMessage" />
  </Form>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

label {
  margin-top: 15px;
  margin-bottom: 8px;

  &.title {
    margin-top: 0;
  }
}

select {
  margin-top: 5px;
}

.char-count {
  display: block;
  font-size: 0.85em;
  float: right;

  color: $background-80;
  margin-top: 5px;
}


.submit-button {
  margin-top: 20px;
}
.error {
  margin-top: 20px;
}

</style>
