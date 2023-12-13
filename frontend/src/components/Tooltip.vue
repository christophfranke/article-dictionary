<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted, onBeforeUnmount } from 'vue';
import type { DictionaryCollection } from '../dictionary/collection';

const props = defineProps({
	dictionary: {
		type: Object as unknown as () => DictionaryCollection,
		required: true,
	},
	highlightedWord: {
		type: String,
		required: true
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
const isVisible = computed(() => !!props.highlightedWord
    && showStatus.value.includes(props.dictionary.find(props.highlightedWord?.toLowerCase() || '')?.status || '')
);

const content = computed(() => isVisible.value
  ? (props.dictionary.find(props.highlightedWord?.toLowerCase() || '')?.translations.join(', ') || '')
  : ''
);

const position = reactive({ x: 0, y: 0 });
const setTooltipPosition = (event: MouseEvent): void => {
  position.x = event.clientX + 10; // Add an offset to prevent the tooltip from overlapping with the cursor
  position.y = event.clientY + 20; // Adjust the offset based on your design preference
};

// time how long a translation is shown
const UPDATE_TIME = 500
let timer = 0
let original = ''
let timeoutId: ReturnType<typeof setTimeout> | null = null
watch(isVisible, (newValue, oldValue) => {
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
  if (!oldValue && newValue) {
    original = props.highlightedWord;
    timer = Date.now();
    timeoutId = setTimeout(() => {
      if (props.display.update.seen && props.dictionary.find(original)?.status === 'new') {
        props.dictionary.updateWord(original, { status: 'seen' });
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

<style scoped>
.tooltip {
  position: fixed;
  z-index: 9999;
  background-color: #333;
  color: #fff;
  padding: 5px;
  border-radius: 5px;
  font-size: 14px;
  pointer-events: none; /* Ensures tooltip doesn't interfere with mouse events */
}

/* Optional: Add some animation for the tooltip */
.tooltip-enter-active, .tooltip-leave-active {
  transition: opacity 0.5s;
}

.tooltip-enter, .tooltip-leave-to {
  opacity: 0;
}
</style>