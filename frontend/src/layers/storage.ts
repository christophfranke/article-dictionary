import { watchEffect } from 'vue';
import type { ComputedRef } from 'vue';
import type { Collection } from './collection';

export interface CollectionXX<T extends { id: string } & Record<K, any> & Record<L, any>, K extends keyof T, L extends keyof T> {
  find: (keyValue: any) => T | undefined;
  findById: (id: string) => T | undefined;

  all: ComputedRef<T[]>;

  set: (newItems: T[]) => void;
  discard: () => void;

  load: () => Promise<T[] | null>;
  get: (requestId: string) => Promise<T | null>;
  updateMany: (requestIds: string[], data: Record<string, unknown>) => Promise<T[] | null>;
  updateOne: (requestId: string, data: Record<string, unknown>) => Promise<T | null>;
  add: (data: Record<string, unknown>) => Promise<T | null>;

  updateLocal: (updatedItems: T[]) => void;
  removeLocalExcept: (ids: string[]) => void;
}


// export default <T extends { id: string } & Record<K, any>, K extends keyof T, L extends keyof T>(collection: Collection<T, K, L>, key: string): Collection<T, K, L> => {
export default <T extends { id: string } & Record<K, any> & Record<L, any>, K extends keyof T, L extends keyof T, SomeCollection extends Collection<T, K, L>>(collection: SomeCollection, key: string): SomeCollection => {
  const serializedItems = localStorage.getItem(key)
  if (serializedItems) {
    try {
      const items: T[] = JSON.parse(serializedItems)
      collection.set(items)
    } catch(e) {
      console.error('Could not restore collection from local storage:', e)
    }
  }

  watchEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(collection.all.value))
    } catch(e) {
      console.error('Could not save collection to local storage')
      localStorage.clear()
    }
  })

  return collection
}

