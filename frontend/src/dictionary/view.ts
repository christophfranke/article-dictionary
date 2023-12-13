import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { DictionaryCollection } from './collection';
import type { Word, PartialWord } from '@/types';


type FilterFunction = (x: PartialWord) => boolean;

export interface DictionaryView {
  find: (original: string) => Word | undefined;
  isVisible: (original: string) => boolean;
  words: ComputedRef<Word[]>;
  allWords: ComputedRef<Word[]>;

  set: (newWords: PartialWord[]) => void;
  setFilter: (filterFn: FilterFunction) => void;

  load: () => Promise<void>;
  updateMany: (originals: string[], data: Record<string, unknown>) => Promise<void>;
  retranslateWord: (original: string) => Promise<void>;
  updateWord: (original: string, data: Record<string, unknown>) => Promise<void>;
  addWord: (original: string) => Promise<void>;
  rebuild: () => Promise<void>;
}


export default (collection: DictionaryCollection, filterFn: FilterFunction = x => !!x): DictionaryView => {
  const filter = ref(filterFn)

  const isVisible = (orginal: string): boolean => {
    const word = collection.find(orginal);
    if (word) {
      return filter.value(word);
    }

    return false
  }

  return {
    find: collection.find,
    isVisible,
    words: computed(() => collection.allWords.value.filter(filter.value)),
    allWords: collection.allWords,
    set: collection.set,
    setFilter: filterFn => {
      filter.value = filterFn
    },

    load: collection.load,
    updateMany: collection.updateMany,
    retranslateWord: collection.retranslateWord,
    updateWord: collection.updateWord,
    addWord: collection.addWord,
    rebuild: collection.rebuild,
  }
}