import { ref, computed } from 'vue';
import type { ComputedRef } from 'vue';
import type { Api } from './api';

export interface Collection<T extends { id: string }> {
  find: (id: string) => T | undefined;

  all: ComputedRef<T[]>;

  set: (newItems: T[]) => void;
  discard: () => void;

  load: () => Promise<void>;
  updateMany: (ids: string[], data: Record<string, unknown>) => Promise<void>;
  updateOne: (id: string, data: Record<string, unknown>) => Promise<void>;
  add: (data: Record<string, unknown>) => Promise<void>;
}


export default <T extends { id: string }>(request: Api<T>, collection: T[] = []): Collection<T> => {
  const items = ref<T[]>([]);
  const itemsById = ref<Record<string, T>>({});

  const set = (newItems: T[]): void => {
    items.value = newItems as any;
    itemsById.value = newItems.reduce((acc, item) => {
      acc[item.id] = item;
      return acc;
    }, {} as { [key: string]: T });
  };

  const add = async (data: Record<string, unknown>): Promise<void> => {
    const item = await request.add(data);
    if (item) {
      items.value = [...items.value, item] as any;
      itemsById.value[item.id] = item;
    }
  };

  const load = async () => {
    set(await request.list());
  }

  const find = (id: string): T | undefined => itemsById.value[id];

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
    items.value = items.value.map(item => {
      const updatedItem = updatedItems.find(ui => ui.id === item.id);
      return updatedItem ? { ...item, ...updatedItem } : item;
    });

    updatedItems.forEach(item => itemsById.value[item.id] = { ...itemsById.value[item.id], ...item });
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
