import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { DictionaryApi } from './request';
import type { PartialWord } from '@/types';
import type { Collection } from '@/layers/collection';
import createCollection from '@/layers/collection';

export interface DictionaryCollection extends Collection<PartialWord, 'original'> {
  retranslate: (original: string) => Promise<void>;
  rebuild: () => Promise<void>;
}


export default (request: DictionaryApi, words: PartialWord[] = []): DictionaryCollection => {
  const collection = createCollection<PartialWord, 'original'>(request, 'original', words);

  const retranslate = async (original: string): Promise<void> => {
    const id = collection.find(original)?.id;
    if (id) {
      for await (const retranslatedWord of request.retranslate(original)) {        
        if (retranslatedWord) {
          collection.updateLocal([retranslatedWord]);
        }      
      }
    }
  };

  const rebuild = async (): Promise<void> => {
    for await (const _ of request.rebuild());
    await collection.load();
  }

  return {
    ...collection,
    retranslate,
    rebuild,
  }
}
