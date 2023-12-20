import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';

import type { Word, PartialWord } from '@/types';
import type { DictionaryCollection } from './collection';
import type { View } from '@/layers/view';
import createView from '@/layers/view';


export type FilterFunction = (x: PartialWord) => boolean;
export type OrderFunction = (x: PartialWord) => number;

export interface DictionaryView extends View<PartialWord, 'original'> {
  retranslate: (original: string) => Promise<void>;
  rebuild: () => Promise<void>;
}


export default (collection: DictionaryCollection, filterFn: FilterFunction = x => !!x, orderFn: OrderFunction | null = null): DictionaryView => {
  const view = createView(collection, filterFn, orderFn)

  return {
    ...view,
    retranslate: collection.retranslate,
    rebuild: collection.rebuild,
  }
}