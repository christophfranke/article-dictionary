import type { ArticleCollection } from './collection';
import createStorage from '@/layers/storage';

export default (collection: ArticleCollection, key: string): ArticleCollection => {
	return createStorage(collection, key);
}
