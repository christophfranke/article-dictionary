<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted, onBeforeUnmount } from 'vue';
import type { PropType } from 'vue';
import type { ArticleBase } from '@/types';
import type { DictionaryView } from '@/dictionary/view';
import { useFetchAuthorized } from '@/use/api';


const props = defineProps({
	dictionary: {
		type: Object as PropType<DictionaryView>,
		required: true,
	},
	highlighted: {
		type: Object as PropType<{ word: string, index: number }>,
		required: true
	},
  article: {
    type: Object as PropType<ArticleBase>,
    default: null,
  },
  display: {
    type: Object,
    default: {
      new: true,
      seen: true,
      known: false,
      update: {
        seen: true
      }
    }
  }
});

const showStatus = computed<string[]>(() => ['new', 'seen', 'known'].filter(status => props.display[status]));
const isVisible = computed(() => !!props.highlighted.word
    && showStatus.value.includes(props.dictionary.find(props.highlighted.word || '')?.status || '')
);

const content = computed(() => isVisible.value
  ? (props.dictionary.find(props.highlighted.word || '')?.translations.join(', ') || '')
  : ''
);

const position = reactive({ x: 0, y: 0 });
const setTooltipPosition = (event: MouseEvent): void => {
  position.x = event.clientX + 10; // Add an offset to prevent the tooltip from overlapping with the cursor
  position.y = event.clientY + 20; // Adjust the offset based on your design preference
};

const fetchAuthorized = useFetchAuthorized();
const markArticleAsSeen = async (article: ArticleBase, index: number) => {
  const result = await fetchAuthorized('/api/articles/seen', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: article.id, index }),
  });
  
  if (result) {
    article.status = 'seen';
  }
}

// time how long a translation is shown
const UPDATE_TIME = 500
let original = ''
let timeoutId: ReturnType<typeof setTimeout> | null = null
watch(isVisible, (newValue, oldValue) => {
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
  if (!oldValue && newValue) {
    original = props.highlighted.word;
    timeoutId = setTimeout(() => {
      if (props.display.update.seen) {
        if (props.dictionary.find(original)?.status === 'new') {
          props.dictionary.updateWord(original, { status: 'seen' });
        }
        if (props.article && props.article.status !== 'read') {
          markArticleAsSeen(props.article, props.highlighted.index);
        }
      }
    }, UPDATE_TIME);
  }
  if (!newValue && oldValue) {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  }
});



onMounted(() => {
  document.addEventListener('mousemove', setTooltipPosition);
});

onBeforeUnmount(() => {
  document.removeEventListener('mousemove', setTooltipPosition);
});
</script>

<template>
  <div v-if="isVisible" class="tooltip" :style="{ top: `${position.y}px`, left: `${position.x}px` }">
		{{ content }}
  </div>	
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

.tooltip {
  position: fixed;
  z-index: 10;
  background-color: $tooltip-background-color;
  color: $tooltip-color;
  padding: 5px;
  border-radius: 5px;
  font-size: $tooltip-font-size;
  pointer-events: none; /* Ensures tooltip doesn't interfere with mouse events */
}
</style>