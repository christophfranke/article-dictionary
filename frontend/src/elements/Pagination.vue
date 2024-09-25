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

const emit = defineEmits(['update:currentPage', 'change']);

const goToFirstPage = () => {
    emit('update:currentPage', 1);
    emit('change');
};

const goToLastPage = () => {
    emit('update:currentPage', props.numberOfPages);
    emit('change');
};

const goToNextPage = () => {
    if (props.numberOfPages > props.currentPage) {
        emit('update:currentPage', props.currentPage + 1);
        emit('change');
    }
};

const goToPreviousPage = () => {
    if (props.currentPage > 1) {
        emit('update:currentPage', props.currentPage - 1);
        emit('change');
    }
};
</script>

<template>
    <div class="pagination">
        <div class="buttons">
            <Button size="small" role="view" @click="goToFirstPage" :disabled="currentPage <= 1">
                <FontAwesomeIcon icon="angles-left" />
            </Button>
            <Button size="small" role="view" @click="goToPreviousPage" :disabled="currentPage <= 1">
                <FontAwesomeIcon icon="angle-left" />
            </Button>
        </div>
        <span>Page {{ currentPage }} of {{ numberOfPages }}</span>
        <div class="buttons">
            <Button size="small" role="view" @click="goToNextPage" :disabled="currentPage >= numberOfPages">
                <FontAwesomeIcon icon="angle-right" />
            </Button>
            <Button size="small" role="view" @click="goToLastPage" :disabled="currentPage >= numberOfPages">
                <FontAwesomeIcon icon="angles-right" />
            </Button>
        </div>
    </div>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}

.buttons {  
  margin: 0 8px;
}
.pagination button {
  margin: 0 2px;
}
</style>
