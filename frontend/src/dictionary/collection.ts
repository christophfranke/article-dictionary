import { ref } from 'vue';
import * as DictionaryRequest from './request';

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
  get: () => Word[];
  set: (newWords: PartialWord[]) => void;
  retranslate: (original: string) => Promise<void>;
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
      updateLocalCollection([updatedWord]);
    }
  };

  const updateMany = async (originals: string[], data: Record<string, unknown>): Promise<void> => {
    const updatedWords = await DictionaryRequest.updateMany(originals, data);
    if (updatedWords) {
      updateLocalCollection(updatedWords);
    }
  };

  const updateLocalCollection = (updatedWords: Word[]): void => {
    words.value = [...words.value.map(word => updatedWords.find(updatedWord => updatedWord.original === word.original)
      ? {
        ...word,
        ...updatedWords.find(updatedWord => updatedWord.original === word.original)
      } : word
    )];
  }

  const retranslateWord = async (original: string): Promise<void> => {
    const retranslatedWord = await DictionaryRequest.retranslate(original);
    if (retranslatedWord) {
      words.value = [...words.value.map(word => word.original === retranslatedWord.original
        ? {
          ...word,
          ...retranslatedWord
        } : word
      )];
    }
  };

  return {
    find: (original: string): Word | undefined => words.value.find(word => word.original === original),
    get: () => words.value.filter(filter.value),
    all: () => words.value,
    set,
    load,
    updateMany,
    retranslateWord,
    updateWord,
    addWord,
    filter: filterFn => {
      filter.value = filterFn
    }
  }
}
