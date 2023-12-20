import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';

import type { Collection } from './collection';

export type FilterFunction<T> = (x: T) => boolean;
export type OrderFunction<T> = (x: T) => number;

export type WithOrder<T> = T & {
  order: number
}

export interface View<T extends { id: string } & Record<K, any> & Record<L, any>, K extends keyof T, L extends keyof T> {
  find: (keyValue: any) => T | undefined;
  
  isVisible: (keyValue: string) => boolean;
  items: ComputedRef<WithOrder<T>[]>;
  all: ComputedRef<WithOrder<T>[]>;

  setFilter: (filterFn: FilterFunction<T>) => void;
  setOrder: (orderFn: OrderFunction<T>) => void;
  discard: () => void;

  load: () => Promise<void>;
  get: (requestId: string) => Promise<void>;
  updateMany: (requestIds: string[], data: Record<string, unknown>) => Promise<void>;
  updateOne: (requestId: string, data: Record<string, unknown>) => Promise<void>;
  add: (data: Record<string, unknown>) => Promise<void>;
}

export default <T extends { id: string } & Record<K, any> & Record<L, any>, K extends keyof T, L extends keyof T>(
  collection: Collection<T, K, L>,
  filterFn: FilterFunction<T> = x => !!x,
  orderFn: OrderFunction<T> | null = null
): View<T, K, L> => {
  const filter = ref(filterFn);
  const order = ref<OrderFunction<T> | null>(orderFn);

  const isVisible = (keyValue: string): boolean => {
    const item = collection.find(keyValue);
    return item ? filter.value(item) : false;
  };

  const all = computed(() => collection.all.value.map((item, index) => ({
    ...item,
    order: order.value ? order.value(item) ?? index : index,
  })));
  const items = computed(() => all.value.filter(filter.value));

  const setOrder = (orderFn?: OrderFunction<T>) => {
    order.value = orderFn || null;
  }

  return {
    ...collection,
    isVisible,
    items,
    all,
    setFilter: fn => { filter.value = fn; },
    setOrder,
  }
}
