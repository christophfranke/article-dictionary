import { watchEffect } from 'vue';
import type { Collection } from './collection';

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

