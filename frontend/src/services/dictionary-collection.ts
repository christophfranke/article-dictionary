import { ref } from 'vue';
import * as DictionaryRequest from './dictionary-request';

export interface PartialWord {
  id: string;
  index: number;
  original: string;
  translations: string[];
  status: string;
}

export interface Word extends PartialWord {
  index: number;
}
type FilterFunction = (x: PartialWord) => boolean;

export interface DictionaryCollection {
  find: (original: string) => Word | undefined;
  get: (additionalFilter?: () => boolean) => Word[];
  set: (newWords: PartialWord[]) => void;
  load: () => Promise<void>;
  updateWord: (original: string, data: Record<string, unknown>) => Promise<void>;
  addWord: (original: string) => Promise<void>;
  filter: (filterFn: FilterFunction) => void;
}



export default (collection: PartialWord[] = [], filterFn: FilterFunction): DictionaryCollection => {
  const words = ref(collection)
  const filter = ref(filterFn)

  const set = newWords => {
    words.value = newWords.map((word, index) => ({ ...word, index }));
  };

  const addWord = async (original: string): Promise<void> => {
    const addedWord = await DictionaryRequest.addWord(original);
    if (addedWord) {
      words.value = [...words.value, addedWord];
    }
  };

  const load = async () => {
    words.value = await DictionaryRequest.loadAll();
  }

  const updateWord = async (original: string, data: Record<string, unknown>): Promise<void> => {
    const updatedWord = await DictionaryRequest.updateWord(original, data);
    if (updatedWord) {
      words.value = [...words.value.map(word => word.original === updatedWord.original
        ? {
          ...word,
          ...updatedWord
        } : word
      )];
    }
  };

  return {
    find: (original: string): Word | undefined => words.value.find(word => word.original === original),
    get: (additionalFilter = () => true) => words.value.filter(filter.value).filter(additionalFilter),
    set,
    load,
    updateWord,
    addWord,
    filter: filterFn => {
      filter.value = filterFn
    }
  }
}
