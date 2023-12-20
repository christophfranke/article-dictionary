import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { DictionaryApi } from './request';
import type { PartialWord } from '@/types';

export interface DictionaryCollection {
  find: (original: string) => PartialWord | undefined;
  allWords: ComputedRef<PartialWord[]>;

  set: (newWords: PartialWord[]) => void;
  discard: () => void;

  load: () => Promise<void>;
  updateMany: (originals: string[], data: Record<string, unknown>) => Promise<void>;
  retranslateWord: (original: string) => Promise<void>;
  updateWord: (original: string, data: Record<string, unknown>) => Promise<void>;
  addWord: (original: string) => Promise<void>;
  rebuild: () => Promise<void>;
}


export default (request: DictionaryApi, collection: PartialWord[] = []): DictionaryCollection => {
  const words = ref<PartialWord[]>([])
  const wordsByOriginal = ref<{
    [key: string]: PartialWord;
  }>({})

  const set = (newWords: PartialWord[]): void => {
    words.value = newWords.map(word => word); // make a new collection
    wordsByOriginal.value ={}
    words.value.forEach(word => wordsByOriginal.value[word.original] = word)
  };

  const addWord = async (original: string): Promise<void> => {
    const addedWord = await request.add({ original });
    if (addedWord) {
      words.value = [...words.value, addedWord];
      wordsByOriginal.value[addedWord.original] = addedWord;
    }
  };

  const load = async () => {
    set(await request.list());
  }

  const find = (original: string): PartialWord | undefined => wordsByOriginal.value[original]

  const updateWord = async (original: string, data: Record<string, unknown>): Promise<void> => {
    const word = find(original)
    if (word) {
      // update local collection
      Object.assign(word, data)

      // update remote collection
      const id = word.id;
      if (id) {      
        const updatedWord = await request.updateOne(id, data);
        if (updatedWord) {
          // keep in sync with remote collection
          updateLocalCollection([updatedWord]);
        }
      }
    }
  };

  const updateMany = async (originals: string[], data: Record<string, unknown>): Promise<void> => {
    const ids = originals.map(original => find(original)?.id!).filter(id => id);
    const updatedWords = await request.updateMany(ids, data);
    if (updatedWords) {
      updateLocalCollection(updatedWords);
    }
  };

  const updateLocalCollection = (updatedWords: PartialWord[]): void => {
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
    const id = find(original)?.id;
    if (id) {
      const retranslatedWord = await request.retranslate(original);
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
    const newCollection = await request.list();
    if (newCollection) {
      set(newCollection);
    }
  }

  set(collection);

  return {
    find,
    allWords: computed(() => words.value),
    set,
    discard: () => set([]),
    load,
    updateMany,
    retranslateWord,
    updateWord,
    addWord,
    rebuild,
  }
}
