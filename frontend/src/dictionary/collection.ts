import { ref } from 'vue';
import * as DictionaryRequest from './request';
import type { Word, PartialWord } from '../types';

type FilterFunction = (x: PartialWord) => boolean;

export interface DictionaryCollection {
  find: (original: string) => Word | undefined;
  get: () => Word[];
  set: (newWords: PartialWord[]) => void;
  all: () => Word[];
  updateMany: (originals: string[], data: Record<string, unknown>) => Promise<void>;
  retranslateWord: (original: string) => Promise<void>;
  load: () => Promise<void>;
  updateWord: (original: string, data: Record<string, unknown>) => Promise<void>;
  addWord: (original: string) => Promise<void>;
  filter: (filterFn: FilterFunction) => void;
}



export default (collection: PartialWord[] = [], filterFn: FilterFunction): DictionaryCollection => {
  const words = ref<Word[]>([])
  const wordsByOriginal = ref<{
    [key: string]: Word;
  }>({})
  const filter = ref(filterFn)

  const set = (newWords: PartialWord[]): void => {
    words.value = newWords.map((word, index) => ({ ...word, index }));
    wordsByOriginal.value = words.value.reduce((acc, word) => ({ ...acc, [word.original]: word }), {});
  };

  const addWord = async (original: string): Promise<void> => {
    const addedWord = await DictionaryRequest.addWord(original.toLowerCase());
    if (addedWord) {
      words.value = [...words.value, addedWord];
      wordsByOriginal.value[addedWord.original] = addedWord;
    }
  };

  const load = async () => {
    set(await DictionaryRequest.loadAll());
  }

  const find =  (original: string): Word | undefined => wordsByOriginal.value[original.toLowerCase()]

  const updateWord = async (original: string, data: Record<string, unknown>): Promise<void> => {
    const id = find(original.toLowerCase())?.id;
    if (id) {      
      const updatedWord = await DictionaryRequest.updateWord(id, data);
      if (updatedWord) {
        updateLocalCollection([updatedWord]);
      }
    }
  };

  const updateMany = async (originals: string[], data: Record<string, unknown>): Promise<void> => {
    const ids = originals.map(original => find(original.toLowerCase())?.id).filter(id => id);
    const updatedWords = await DictionaryRequest.updateMany(ids, data);
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
    updatedWords.forEach(word => wordsByOriginal.value[word.original] = {
      ...wordsByOriginal.value[word.original],
      ...word
    });
  }

  const retranslateWord = async (original: string): Promise<void> => {
    const id = find(original.toLowerCase())?.id;
    if (id) {
      const retranslatedWord = await DictionaryRequest.retranslate(original.toLowerCase());
      if (retranslatedWord) {
        words.value = [...words.value.map(word => word.original === retranslatedWord.original
          ? {
            ...word,
            ...retranslatedWord
          } : word
        )];
        wordsByOriginal.value[retranslatedWord.original] = {
          ...wordsByOriginal.value[retranslatedWord.original],
          ...retranslatedWord
        };
      }      
    }
  };

  set(collection);

  return {
    find,
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
