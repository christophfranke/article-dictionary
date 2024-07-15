import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { StreamApi } from './api';

export interface Collection<T extends { id: string } & Record<K, any> & Record<L, any>, K extends keyof T, L extends keyof T> {
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
}


export default <T extends { id: string } & Record<K, any>, K extends keyof T, L extends keyof T>(request: StreamApi<T>, searchField: K, requestField: L): Collection<T, K, L> => {
  const items = ref<T[]>([]);
  const itemsByKey = ref<Record<string, T>>({});
  const itemsById = ref<Record<string, T>>({});

  const set = (newItems: T[]): void => {
    items.value = newItems as any;
    itemsByKey.value = {}
    itemsById.value = {}
    for(const item of newItems) {
      itemsByKey.value[item[searchField]] = item
      itemsById.value[item.id] = item
    }
  };

  const add = async (data: Record<string, unknown>): Promise<T | null> => {
    let result = null;
    for await (const item of request.add(data)) {
      // console.log('adding', item)
      if (item) {
        result = item;
        if (itemsByKey.value[item[searchField]]) {
          const original = itemsByKey.value[item[searchField]]
          delete itemsById.value[original.id]
          Object.assign(original, item)
          itemsById.value[original.id] = original
          items.value = items.value
        } else if (itemsById.value[item.id]) {
          const original = itemsById.value[item.id]
          delete itemsByKey.value[original[searchField]]
          Object.assign(original, item)
          itemsByKey.value[original[searchField]] = original
          items.value = items.value
        } else {
          items.value = [...items.value, item] as any;
          itemsByKey.value[item[searchField]] = item;
          itemsById.value[item.id] = item;
        }
      }
    }

    return result;
  };

  const load = async (): Promise<T[] | null> => {
    let result = null;
    for await (const itemList of request.list()) {
      set(itemList);
      result = itemList;
    }

    return result;
  }

  const find = (searchValue: any): T | undefined => itemsByKey.value[searchValue];
  const findById = (id: any): T | undefined => itemsById.value[id];

  const updateOne = async (requestId: string, data: Record<string, unknown>): Promise<T | null> => {
    let result = null;
    for await (const updatedItem of request.updateOne(requestId, data)) {        
      if (updatedItem) {
        result = updatedItem;
        updateLocal([updatedItem]);
      }
    }

    return result;
  };

  const updateMany = async (requestIds: string[], data: Record<string, unknown>): Promise<T[] | null> => {
    let result = null;
    for await (const updatedItems of request.updateMany(requestIds, data)) {
      if (updatedItems) {
        result = updatedItems;
        updateLocal(updatedItems);
      }
    }

    return result;
  };

  const get = async (requestId: string): Promise<T | null> => {
    let result = null;
    for await (const updatedItem of request.get(requestId)) {
      if (updatedItem) {
        result = updatedItem;
        updateLocal([updatedItem]);
      }
    }

    return result;
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

  const discard = () => {
    items.value = [];
    itemsByKey.value = {};
    itemsById.value = {};
  }

  const all = computed<T[]>(() => {
    // console.log('collection', items.value.length)
    return items.value
  });

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
  }
}
