import type { DictionaryCollection } from './collection';
import createStorage from '@/layers/storage';

export default (collection: DictionaryCollection, key: string): DictionaryCollection => {
	return createStorage(collection, key);
}
