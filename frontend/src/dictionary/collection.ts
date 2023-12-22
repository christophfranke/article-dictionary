import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { DictionaryApi } from './request';
import type { PartialWord } from '@/types';
import type { Collection } from '@/layers/collection';
import createCollection from '@/layers/collection';

export interface DictionaryCollection extends Collection<PartialWord, 'original', 'id'> {
  retranslate: (original: string) => Promise<void>;
  rebuild: () => Promise<void>;
}


export default (request: DictionaryApi, words: PartialWord[] = []): DictionaryCollection => {
  const collection = createCollection<PartialWord, 'original', 'id'>(request, 'original', 'id');

  const retranslate = async (id: string): Promise<void> => {
    for await (const retranslatedWord of request.retranslate(id)) {        
      if (retranslatedWord) {
        collection.updateLocal([retranslatedWord]);
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
