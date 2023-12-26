import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { DictionaryApi } from './request';
import type { PartialWord } from '@/types';
import type { Collection } from '@/layers/collection';
import createCollection from '@/layers/collection';

export interface DictionaryCollection extends Collection<PartialWord, 'original', 'id'> {
  retranslate: (original: string) => Promise<PartialWord | null>;
  rebuild: () => Promise<PartialWord[] | null>;
  markSeen: (id: string) => Promise<PartialWord | null>;
}


export default (request: DictionaryApi, words: PartialWord[] = []): DictionaryCollection => {
  const collection = createCollection<PartialWord, 'original', 'id'>(request, 'original', 'id');

  const retranslate = async (id: string): Promise<PartialWord | null> => {
    let result = null;
    for await (const retranslatedWord of request.retranslate(id)) {        
      if (retranslatedWord) {
        collection.updateLocal([retranslatedWord]);
        result = retranslatedWord;
      }
    }

    return result;
  };

  const rebuild = async (): Promise<PartialWord[] | null> => {
    for await (const _ of request.rebuild());
    return await collection.load();
  }

  const markSeen = async (id: string): Promise<PartialWord | null> => {
    let result = null;
    for await (const seenWord of request.markSeen(id)) {
      if (seenWord) {
        collection.updateLocal([seenWord]);
        result = seenWord;
      }
    }

    return result;
  };

  return {
    ...collection,
    markSeen,
    retranslate,
    rebuild,
  }
}
