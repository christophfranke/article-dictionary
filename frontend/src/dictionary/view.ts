import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';

import type { Word, PartialWord } from '@/types';
import type { DictionaryCollection } from './collection';
import type { View } from '@/layers/view';
import createView from '@/layers/view';


export type FilterFunction = (x: PartialWord) => boolean;
export type OrderFunction = (x: PartialWord) => number;

export interface DictionaryView extends View<PartialWord, 'original', 'id'> {
  retranslate: (original: string) => Promise<PartialWord | null>;
  rebuild: () => Promise<PartialWord[] | null>;
  markSeen: (id: string) => Promise<PartialWord | null>;
}


export default (collection: DictionaryCollection, filterFn: FilterFunction = x => !!x, orderFn: OrderFunction | null = null): DictionaryView => {
  const view = createView(collection, filterFn, orderFn)

  return {
    ...collection,
    ...view,
  }
}