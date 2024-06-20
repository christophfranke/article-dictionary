<script setup lang="ts">
import type { PropType } from 'vue';
import Button from '@/elements/Button.vue';
import ErroMessage from '@/elements/ErrorMessage.vue';

import __ from '@/i18n'

const props = defineProps({
  articleStatus: String,
  isLoadingButton: Boolean,
  errorMessage: String as PropType<string | null>,
});

const emit = defineEmits(['markAsRead']);

const onMarkAsRead = () => {
  emit('markAsRead');
};
</script>

<template>
  <div>
    <Button
      v-if="props.articleStatus !== 'read'"
      :disabled="props.isLoadingButton"
      class="mark-as-read"
      @click="onMarkAsRead"
    >{{__('Mark as read')}}</Button>
    <ErroMessage :message="props.errorMessage" />
  </div>
</template>

<style scoped>
.mark-as-read {
  margin-top: 30px;
}

.error {
  margin-top: 20px;
}
</style>
