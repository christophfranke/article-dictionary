<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import Button from '@/elements/Button.vue';
import InternalLink from '@/elements/InternalLink.vue';

const props = defineProps({
  numberOfPages: {
    type: Number,
    required: true
  },
  currentPage: {
    type: Number,
    required: true,
  }
});

const emit = defineEmits(['update:currentPage']);

const goToNextPage = () => {
  if (props.numberOfPages > props.currentPage) {
    emit('update:currentPage', props.currentPage + 1);
  }
};

const goToPreviousPage = () => {
  if (props.currentPage > 1) {
    emit('update:currentPage', props.currentPage - 1);
  }
};
</script>

<template>
  <div class="pagination">
    <Button size="small" role="view" @click="goToPreviousPage" :disabled="currentPage <= 1">
      <FontAwesomeIcon icon="chevron-left" />
    </Button>
    <span>Page {{ currentPage }} of {{ numberOfPages }}</span>
    <Button size="small" role="view" @click="goToNextPage" :disabled="currentPage >= numberOfPages">
      <FontAwesomeIcon icon="chevron-right" />
    </Button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination button {
  margin: 0 10px;
}
</style>
