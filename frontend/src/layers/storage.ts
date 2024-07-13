import type { StreamApi } from './api';

export default <T extends { id: string }>(request: StreamApi<T>, key: string): StreamApi<T> => {
  let collection: { [key: string]: T } = JSON.parse(localStorage.getItem(key) || '{}');

  const save = (newData: T[]) => {
    newData.forEach(item => {
      if (item.id in collection) {
        Object.assign(collection[item.id], item);
      } else {
        collection[item.id] = item;
      }
    });
    try {
      localStorage.setItem(key, JSON.stringify(collection));
    } catch (e) {
      localStorage.clear();
      console.error('could not save collection to local storage', e);
    }
  };

  const list = async function* (): AsyncGenerator<T[], void, unknown> {
    yield Object.values(collection);
    for await (const newData of request.list()) {
      yield newData;
      save(newData);
    }
  };

  const add = async function* (data: Record<string, unknown>): AsyncGenerator<T | null, void, unknown> {
    for await (const newData of request.add(data)) {
      yield newData;
      if (newData) {
        save([newData]);
      }
    }
  };

  const get = async function* (id: string): AsyncGenerator<T | null, void, unknown> {
    const item = collection[id];
    if (item) {
      yield item;
    }
    for await(const newItem of request.get(id)) {
      yield newItem;
      if (newItem) {
        save([newItem]);
      }
    }
  };

  const updateOne = async function* (id: string, data: Record<string, unknown>): AsyncGenerator<T | null, void, unknown> {
    const oldItem = collection[id];
    if (oldItem) {
      const item = { ...oldItem, ...data } as T;
      yield item;
      save([item]);
    }

    for await (const newData of request.updateOne(id, data)) {
      yield newData;
      if (newData) {
        save([newData]);
      }
    }
  };

  return {
    ...request,
    add,
    get,
    updateOne,
    list
  };
};
