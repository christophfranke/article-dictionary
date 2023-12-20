import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { StreamApi } from './api';

export interface Collection<T extends { id: string } & Record<K, any> & Record<L, any>, K extends keyof T, L extends keyof T> {
  find: (keyValue: any) => T | undefined;
  findById: (id: string) => T | undefined;

  all: ComputedRef<T[]>;

  set: (newItems: T[]) => void;
  discard: () => void;

  load: () => Promise<void>;
  updateMany: (ids: string[], data: Record<string, unknown>) => Promise<void>;
  updateOne: (id: string, data: Record<string, unknown>) => Promise<void>;
  add: (data: Record<string, unknown>) => Promise<void>;
  updateLocal: (updatedItems: T[]) => void;
}


export default <T extends { id: string } & Record<K, any>, K extends keyof T, L extends keyof T>(request: StreamApi<T>, searchField: K, requestField: L): Collection<T, K, L> => {
  const items = ref<T[]>([]);
  const itemsByKey = ref<Record<string, T>>({});
  const itemsById = ref<Record<string, T>>({});

  const set = (newItems: T[]): void => {
    items.value = newItems as any;
    itemsByKey.value = newItems.reduce((acc, item) => {
      acc[item[searchField]] = item;
      return acc;
    }, {} as Record<string, T>);
    itemsById.value = newItems.reduce((acc, item) => {
      acc[item.id] = item;
      return acc;
    }, {} as Record<string, T>);
  };

  const add = async (data: Record<string, unknown>): Promise<void> => {
    for await (const item of request.add(data)) {      
      if (item) {
        if (!itemsByKey.value[item[searchField]]) {          
          items.value = [...items.value, item] as any;
          itemsByKey.value[item[searchField]] = item;
          itemsById.value[item.id] = item;
        } else {
          updateLocal([item]);
        }
      }
    }
  };

  const load = async () => {
    for await (const items of request.list()) {
      set(items);
    }
  }

  const find = (searchValue: any): T | undefined => itemsByKey.value[searchValue];
  const findById = (id: any): T | undefined => itemsById.value[id];

  const updateOne = async (id: string, data: Record<string, unknown>): Promise<void> => {
    const item = findById(id);
    if (item) {
      for await (const updatedItem of request.updateOne(item[requestField], data)) {        
        if (updatedItem) {
          updateLocal([updatedItem]);
        }
      }
    }
  };

  const updateMany = async (ids: string[], data: Record<string, unknown>): Promise<void> => {
    const requestParams = ids
      .map(id => findById(id))
      .filter(x => !!x)
      .map(x => x![requestField]);
    for await (const updatedItems of request.updateMany(requestParams, data)) {
      if (updatedItems) {
        updateLocal(updatedItems);
      }
    }
  };

  const updateLocal = (updatedItems: T[]): void => {
    updatedItems.forEach(updated => {
      const item = findById(updated.id);
      if (item) {
        Object.assign(item, updated);
      } else {
        items.value.push(updated as any);
        itemsByKey.value[updated[searchField]] = updated;
        itemsById.value[updated.id] = updated;
      }
    });
  }

  return {
    find,
    findById,
    all: computed<T[]>(() => items.value as any),
    set,
    discard: () => set([]),
    load,
    updateMany,
    updateOne,
    add,
    updateLocal
  }
}
