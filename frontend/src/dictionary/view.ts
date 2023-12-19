import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';

import type { Word, PartialWord } from '@/types';
import type { DictionaryCollection } from './collection';


export type FilterFunction = (x: PartialWord) => boolean;
export type OrderFunction = (x: PartialWord) => number;

export interface DictionaryView {
  find: (original: string) => Word | undefined;
  isVisible: (original: string) => boolean;
  words: ComputedRef<Word[]>;
  allWords: ComputedRef<Word[]>;

  set: (newWords: PartialWord[]) => void;
  setFilter: (filterFn: FilterFunction) => void;
  setOrder: (orderFn: OrderFunction) => void;
  discard: () => void;

  load: () => Promise<void>;
  updateMany: (originals: string[], data: Record<string, unknown>) => Promise<void>;
  retranslateWord: (original: string) => Promise<void>;
  updateWord: (original: string, data: Record<string, unknown>) => Promise<void>;
  addWord: (original: string) => Promise<void>;
  rebuild: () => Promise<void>;
}


export default (collection: DictionaryCollection, filterFn: FilterFunction = x => !!x, orderFn: OrderFunction | null = null): DictionaryView => {
  const filter = ref(filterFn);
  const order = ref<OrderFunction | null>(orderFn);

  const isVisible = (orginal: string): boolean => {
    const word = collection.find(orginal);
    if (word) {
      return filter.value(word);
    }

    return false;
  }

  const allWords = computed(() => collection.allWords.value as unknown as Word[]);
  const words = computed(() => allWords.value.filter(filter.value) as unknown as Word[]);
  const find = (original: string) => collection.find(original) as unknown as Word | undefined;

  const setOrder = (orderFn?: OrderFunction) => {
    order.value = orderFn || null;
    if (orderFn) {
      allWords.value.forEach((word, index) => {
        word.order = orderFn(word) ?? index;
      });
    } else {
      allWords.value.forEach((word, index) => {
        word.order = index;
      });
    }
  }

  const set = (newWords: PartialWord[]): void => {
    collection.set(newWords);
    setOrder(order.value);
  }

  return {
    find,
    isVisible,
    words,
    allWords,
    set,
    discard: collection.discard,
    setFilter: filterFn => {
      filter.value = filterFn
    },
    setOrder,

    load: collection.load,
    updateMany: collection.updateMany,
    retranslateWord: collection.retranslateWord,
    updateWord: collection.updateWord,
    addWord: collection.addWord,
    rebuild: collection.rebuild,
  }
}