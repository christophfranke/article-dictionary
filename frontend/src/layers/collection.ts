import { ref, computed } from 'vue';
import type { ComputedRef, Ref } from 'vue';
import type { StreamApi } from './api';

export interface Collection<T extends { id: string } & Record<K, any> & Record<L, any>, K extends keyof T, L extends keyof T> {
  find: (keyValue: any) => T | undefined;
  findById: (id: string) => T | undefined;

  all: ComputedRef<T[]>;

  set: (newItems: T[]) => T[];
  discard: () => void;

  load: () => Promise<T[] | null>;
  get: (requestId: string) => Promise<T | null>;
  updateMany: (requestIds: string[], data: Record<string, unknown>) => Promise<T[] | null>;
  updateOne: (requestId: string, data: Record<string, unknown>) => Promise<T | null>;
  add: (data: Record<string, unknown>) => Promise<T | null>;

  updateLocal: (updatedItems: T[]) => void;
}


const assign = <T>(original: T, updated: T) => {
  if (!updated) {
    // console.log('no update')
    return
  }

  if (!original) {
    // console.log('no original')
    return {
      ...updated
    }
  }

  for(const [key, value] of Object.entries(updated)) {
      // @ts-expect-error
    if (typeof value === 'object' && typeof original[key] === 'object') {
      // @ts-expect-error
      assign(original[key], value)
      // @ts-expect-error
    } else if (original[key] !== value) {
      // console.log('assign key', key)
      // @ts-expect-error
      original[key] = value
    }
  }
}



export default <T extends { id: string } & Record<K, any>, K extends keyof T, L extends keyof T>(request: StreamApi<T>, searchField: K, requestField: L): Collection<T, K, L> => {
  const items: Ref<T[]> = ref<T[]>([]);
  const itemsByKey = ref<Record<string, T>>({});
  const itemsById = ref<Record<string, T>>({});

  // this algorithm ensures to never throw away the old references
  // it is carefully crafted to have linear runtime
  const set = (newItems: T[]): T[] => {
    // generate id map
    const idMap: Record<string, T> = {}
    newItems.forEach(item => {
      idMap[item.id] = item
    })

    // add new items
    newItems.forEach(item => {
      if (!itemsById.value[item.id]) {
        // @ts-expect-error
        itemsById.value[item.id] = {}
      }
      assign(itemsById.value[item.id], item)
    })

    // delete old items
    Object.keys(itemsById.value).forEach(id => {
      if (!idMap[id]) {
        delete itemsById.value[id]
      }
    })

    items.value = Object.values(itemsById.value)

    // fill key map
    itemsByKey.value = {}
    items.value.forEach(item => {
      if (item[searchField] !== undefined) {
        itemsByKey.value[item[searchField]] = item
      }
    })

    return items.value
  };

  const add = async (data: Record<string, unknown>): Promise<T | null> => {
    let result = null;
    for await (const item of request.add(data)) {
      if (item) {
        result = item;
        if (itemsByKey.value[item[searchField]]) {
          const original = itemsByKey.value[item[searchField]]
          delete itemsById.value[original.id]
          assign(original, item)
          itemsById.value[original.id] = original
          items.value = items.value
        } else if (itemsById.value[item.id]) {
          const original = itemsById.value[item.id]
          delete itemsByKey.value[original[searchField]]
          assign(original, item)
          itemsByKey.value[original[searchField]] = original
          items.value = items.value
        } else {
          items.value.push(item as any);
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
      const mergedList = itemList.map((newItem: T) => {
        const oldItem = findById(newItem.id) || {}
        return {
          ...oldItem,
          ...newItem
        }
      })

      result = set(itemList);
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
        const item = findById(updated.id) || find(updated[searchField]);
        if (item) {
          assign(item, updated);
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
