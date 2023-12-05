import { ref } from 'vue';
import * as DictionaryRequest from './dictionary-request';

export default (collection: Word[] = [], filterFn: Function = x => true) => {
  const words = ref(collection)
  const filter = ref(filterFn)

  const addWord = async (original: string): Promise<void> => {
    const addedWord = DictionaryRequest.addWord(newWord.value);
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
        ? updatedWord
        : word
      )];
    }
  };

  return {
    find: (original: string): Word | undefined => words.value.find(word => word.original === original),
    get: (additionalFilter = () => true) => words.value.filter(filter.value).filter(additionalFilter),
    set: newWords => {
      words.value = newWords
    },
    load,
    updateWord,
    addWord,
    filter: filterFn => {
      filter.value = filterFn
    }
  }
}
