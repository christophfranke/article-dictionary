import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';

import type { Word, PartialWord, WordDetail } from '@/types';
import type { DictionaryCollection } from './collection';
import type { View } from '@/layers/view';
import createView from '@/layers/view';


function isWord(word: PartialWord): word is Word {
  return (word as Word).order !== undefined;
}

function isWordDetail(word: PartialWord): word is WordDetail {
  const asWordDetail = word as WordDetail;
  return asWordDetail.sentences !== undefined && asWordDetail.similar !== undefined;
}


export type FilterFunction = (x: PartialWord) => boolean;
export type OrderFunction = (x: PartialWord) => number;

export interface DictionaryView extends View<PartialWord, 'original', 'id'> {
  retranslate: (original: string) => Promise<PartialWord | null>;
  rebuild: () => Promise<PartialWord[] | null>;
  markSeen: (id: string) => Promise<PartialWord | null>;
  detail: (original: string) => ComputedRef<WordDetail | undefined>;
  getWord: (id: string) => Promise<PartialWord | null>;
}


export default (collection: DictionaryCollection, filterFn: FilterFunction = x => !!x, orderFn: OrderFunction | null = null): DictionaryView => {
  const view = createView(collection, filterFn, orderFn)

  const detail = (original: string): ComputedRef<WordDetail | undefined> => computed<WordDetail | undefined>(() => {
    const word = view.find(original);
    if (word) {
      return isWordDetail(word) ? word : undefined
    }

    return undefined
  });

  return {
    ...collection,
    ...view,
    detail
  }
}