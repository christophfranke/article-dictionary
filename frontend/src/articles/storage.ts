import type { ArticleBase } from '@/types';
import type { ArticleApi } from './api';
import createStorage from '@/layers/storage';

export default (api: ArticleApi, key: string): ArticleApi => {
	const storage = createStorage(api, key);

	return {
		...api,
		...storage
	}
}
