import type { StreamApi } from './api';

export default <T extends { id: string }>(request: StreamApi<T>, key: string): StreamApi<T> => {
  let cache: { [key: string]: T } = JSON.parse(localStorage.getItem(key) || '{}');

  const clearcache = () => {
    cache = {}
  }

  const save = (newData: T[]) => {
    newData.forEach(item => {
      if (item.id in cache) {
        Object.assign(cache[item.id], item);
      } else {
        cache[item.id] = item;
      }
    });
    try {
      localStorage.setItem(key, JSON.stringify(cache));
      // console.log('saved items to', key, Object.keys(cache).length)
    } catch (e) {
      localStorage.clear();
      console.error('could not save cache to local storage', e);
    }
  };

  const list = async function* (): AsyncGenerator<T[], void, unknown> {
    yield Object.values(cache);
    for await (const newData of request.list()) {
      clearcache()
      yield newData;
      // console.log('saving list to local storage', newData.length)
      save(newData);
    }
  };

  const add = async function* (data: Record<string, unknown>): AsyncGenerator<T | null, void, unknown> {
    for await (const newData of request.add(data)) {
      yield newData;
      // console.log('saving item to local storage', newData)
      if (newData) {
        save([newData]);
      }
    }
  };

  const get = async function* (id: string): AsyncGenerator<T | null, void, unknown> {
    const item = cache[id];
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
    const oldItem = cache[id];
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
