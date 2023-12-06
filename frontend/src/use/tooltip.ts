import { ref, onMounted, onBeforeUnmount, reactive, computed } from 'vue';

interface TooltipPosition {
  x: number;
  y: number;
}

interface TooltipOptions {
  highlightedWord: Ref<string | undefined>;
  dictionary: Dictionary;
}

interface TooltipResult {
  position: TooltipPosition;
  content: ComputedRef<string>;
  isVisible: ComputedRef<boolean>;
}

interface Word {
  original: string;
  translations: string[];
}

interface Dictionary {
  find(original: string): Word | undefined;
}

const useTooltip = (options: TooltipOptions): TooltipResult => {
  const { highlightedWord, dictionary } = options;

  const position = reactive({ x: 0, y: 0 });

  const isVisible = computed(() => !!highlightedWord
      && ['new', 'seen'].includes(dictionary.find(highlightedWord.value.toLowerCase())?.status || '')
  );

  const content = computed(() =>
    isVisible.value ? (dictionary.find(highlightedWord.value.toLowerCase())?.translations.join(', ') || '') : ''
  );

  const setTooltipPosition = (event: MouseEvent): void => {
    position.x = event.clientX + 10; // Add an offset to prevent the tooltip from overlapping with the cursor
    position.y = event.clientY + 20; // Adjust the offset based on your design preference
  };

  onMounted(() => {
    document.addEventListener('mousemove', setTooltipPosition);
  });

  onBeforeUnmount(() => {
    document.removeEventListener('mousemove', setTooltipPosition);
  });

  return { position, content, isVisible };
};

export default useTooltip;
