import type { ArticleCollection } from './collection';
import createStorage from '@/layers/storage';

export default (collection: ArticleCollection, key: string): ArticleCollection => {
	// @ts-expect-error
	return createStorage(collection, key);
}
