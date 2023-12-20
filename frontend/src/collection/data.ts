import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { Api } from './api';

export interface Collection<T extends { id: string } & Record<K, string>, K extends keyof T> {
  find: (keyValue: string) => T | undefined;

  all: ComputedRef<T[]>;

  set: (newItems: T[]) => void;
  discard: () => void;

  load: () => Promise<void>;
  updateMany: (ids: string[], data: Record<string, unknown>) => Promise<void>;
  updateOne: (id: string, data: Record<string, unknown>) => Promise<void>;
  add: (data: Record<string, unknown>) => Promise<void>;
}


export default <T extends { id: string } & Record<K, string>, K extends keyof T>(request: Api<T>, searchField: K, collection: T[] = []): Collection<T, K> => {
  const items = ref<T[]>([]);
  const itemsByKey = ref<Record<string, T>>({});

  const set = (newItems: T[]): void => {
    items.value = newItems as any;
    itemsByKey.value = newItems.reduce((acc, item) => {
      acc[item[searchField]] = item;
      return acc;
    }, {} as Record<string, T>);
  };

  const add = async (data: Record<string, unknown>): Promise<void> => {
    const item = await request.add(data);
    if (item) {
      items.value = [...items.value, item] as any;
      itemsByKey.value[item[searchField]] = item;
    }
  };

  const load = async () => {
    set(await request.list());
  }

  const find = (searchValue: string): T | undefined => itemsByKey.value[searchValue];

  const updateOne = async (id: string, data: Record<string, unknown>): Promise<void> => {
    const item = find(id);
    if (item) {
      Object.assign(item, data);

      const updatedItem = await request.updateOne(id, data);
      if (updatedItem) {
        updateLocalCollection([updatedItem]);
      }
    }
  };

  const updateMany = async (ids: string[], data: Record<string, unknown>): Promise<void> => {
    const updatedItems = await request.updateMany(ids, data);
    if (updatedItems) {
      updateLocalCollection(updatedItems);
    }
  };

  const updateLocalCollection = (updatedItems: T[]): void => {
    items.value = items.value.map((item: any) => {
      const updatedItem = updatedItems.find(ui => ui.id === item.id);
      return updatedItem ? { ...item, ...updatedItem } : item;
    });

    updatedItems.forEach(item => itemsByKey.value[item[searchField]] = { ...itemsByKey.value[item[searchField]], ...item });
  }

  set(collection);

  return {
    find,
    all: computed<T[]>(() => items.value as any),
    set,
    discard: () => set([]),
    load,
    updateMany,
    updateOne,
    add,
  }
}
