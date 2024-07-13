<script setup lang="ts">
import { computed, watchEffect } from 'vue';
import type { PropType } from 'vue';
import type { DictionaryView } from '@/dictionary/view';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import DictionaryTable from '@/components/DictionaryTable.vue';
import Button from '@/elements/Button.vue';


const props = defineProps({
  showDictionary: Boolean,
  dictionary: Object as PropType<DictionaryView>,
  highlightedWord: String,
  toggleShowDictionary: Function,
});


const tableDisplayConfig = computed(() => ({
  header: true,
  limit: 0,
  sortBy: 'order',
  sortOrder: 'asc',
  col: {
    number: true,
    original: true,
    translations: true,
    status: false,
    actions: true,
    frequency: false,
  },
  action: {
    known: false,
    ignore: true,
    add: false,
    sort: true,
    edit: true,
    retranslate: true,
    status: false,
    glosbe: true,
    detail: false,
    link: true,
  },
  behaviour: {
    highlight: props.showDictionary,
    scroll: props.showDictionary,
  }
}));

</script>

<template>
  <div class="dictionary-container" :class="{ hidden: !props.showDictionary}" v-if="props.dictionary">
    <Button class="toggle-dictionary-button" @click="props.toggleShowDictionary" role="view">
      <FontAwesomeIcon icon="chevron-right" :class="{ rotate: !props.showDictionary}" />
    </Button>
    <div class="dictionary-scoller">
      <DictionaryTable :dictionary="props.dictionary" :display="tableDisplayConfig" sort="number" :highlight="props.highlightedWord" />
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

.dictionary-container {
  background-color: $background-100;
  position: fixed;
  top: 20px;
  right: 20px;
  max-height: calc(100vh - 40px);
  max-width: 550px;
  padding-bottom: 20px;
  overflow-x: visible;
  transition: transform 0.3s ease;
}

.dictionary-container.hidden {
  transform: translateX(100%);
}

.dictionary-scoller {
  max-height: calc(100vh - 40px);
  overflow-y: auto;
}

.toggle-dictionary-button {
  position: absolute;
  top: 0;
  left: -10px;
  transform: translateX(-100%);
  padding: 10px;

  svg {
    transition: transform 0.3s ease;
  }
  .rotate {
    transform: rotate(180deg);
  }
}
</style>
