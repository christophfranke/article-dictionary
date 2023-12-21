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
  get: (requestId: string) => Promise<void>;
  updateMany: (requestIds: string[], data: Record<string, unknown>) => Promise<void>;
  updateOne: (requestId: string, data: Record<string, unknown>) => Promise<void>;
  add: (data: Record<string, unknown>) => Promise<void>;

  updateLocal: (updatedItems: T[]) => void;
  removeLocalExcept: (ids: string[]) => void;
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
      updateLocal(items);
      removeLocalExcept(items.map(item => item.id));
    }
  }

  const find = (searchValue: any): T | undefined => itemsByKey.value[searchValue];
  const findById = (id: any): T | undefined => itemsById.value[id];

  const updateOne = async (requestId: string, data: Record<string, unknown>): Promise<void> => {
    for await (const updatedItem of request.updateOne(requestId, data)) {        
      if (updatedItem) {
        updateLocal([updatedItem]);
      }
    }
  };

  const updateMany = async (requestIds: string[], data: Record<string, unknown>): Promise<void> => {
    for await (const updatedItems of request.updateMany(requestIds, data)) {
      if (updatedItems) {
        updateLocal(updatedItems);
      }
    }
  };

  const get = async (requestId: string): Promise<void> => {
    for await (const updatedItem of request.get(requestId)) {
      if (updatedItem) {
        updateLocal([updatedItem]);
      }
    }
  };

  const updateLocal = (updatedItems: T[]): void => {
    if (!items.value.length) {
      set(updatedItems);
    } else {
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
  };

  const removeLocalExcept = (keepIds: string[]): void => {
    const removeIds = items.value
      .filter(item => !keepIds.includes(item.id))
      .map(item => item.id);

    items.value = items.value
      .filter(item => keepIds.includes(item.id));
    removeIds.forEach(id => {
      delete itemsByKey.value[id];
      delete itemsById.value[id];
    });
  }

  const discard = () => {
    items.value = [];
    itemsByKey.value = {};
    itemsById.value = {};
  }

  const all = computed<T[]>(() => items.value);

  return {
    find,
    findById,
    all,
    set,
    discard,
    load,
    get,
    updateMany,
    updateOne,
    add,
    updateLocal,
    removeLocalExcept,
  }
}
