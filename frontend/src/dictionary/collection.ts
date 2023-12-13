import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { DictionaryApi } from './request';
import type { Word, PartialWord } from '@/types';

type FilterFunction = (x: PartialWord) => boolean;

export interface DictionaryCollection {
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



export default (request: DictionaryApi, collection: PartialWord[] = [], filterFn: FilterFunction = x => !!x): DictionaryCollection => {
  const words = ref<Word[]>([])
  const wordsByOriginal = ref<{
    [key: string]: Word;
  }>({})
  const filter = ref(filterFn)

  const set = (newWords: PartialWord[]): void => {
    words.value = newWords.map((word, index) => ({ ...word, index }));
    wordsByOriginal.value ={}
    words.value.forEach(word => wordsByOriginal.value[word.original] = word)
  };

  const addWord = async (original: string): Promise<void> => {
    const addedWord = await request.addWord(original.toLowerCase());
    if (addedWord) {
      words.value = [...words.value, addedWord];
      wordsByOriginal.value[addedWord.original] = addedWord;
    }
  };

  const load = async () => {
    set(await request.loadAll());
  }

  const find = (original: string): Word | undefined => wordsByOriginal.value[original.toLowerCase()]
  const isVisible = (orginal: string): boolean => {
    const word = find(orginal);
    if (word) {
      return filter.value(word);
    }

    return false
  }

  const updateWord = async (original: string, data: Record<string, unknown>): Promise<void> => {
    const word = find(original.toLowerCase())
    if (word) {
      // update local collection
      Object.assign(word, data)

      // update remote collection
      const id = word.id;
      if (id) {      
        const updatedWord = await request.updateWord(id, data);
        if (updatedWord) {
          // keep in sync with remote collection
          updateLocalCollection([updatedWord]);
        }
      }
    }
  };

  const updateMany = async (originals: string[], data: Record<string, unknown>): Promise<void> => {
    const ids = originals.map(original => find(original.toLowerCase())?.id!).filter(id => id);
    const updatedWords = await request.updateMany(ids, data);
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
      const retranslatedWord = await request.retranslate(original.toLowerCase());
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

  const rebuild = async (): Promise<void> => {
    await request.rebuild();
    const newCollection = await request.loadAll();
    if (newCollection) {
      set(newCollection);
    }
  }

  set(collection);

  return {
    find,
    isVisible,
    words: computed(() => words.value.filter(filter.value)),
    allWords: computed(() => words.value),
    set,
    load,
    updateMany,
    retranslateWord,
    updateWord,
    addWord,
    rebuild,
    setFilter: filterFn => {
      filter.value = filterFn
    }
  }
}
