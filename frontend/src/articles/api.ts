import type { ArticleBase, FetchFn } from '@/types';
import type { StreamApi } from '@/layers/api'
import { makeAsyncGenerator } from '@/layers/api'

export interface ArticleApi extends StreamApi<ArticleBase> {
	markSeen: (data: Record<string, unknown>) => AsyncGenerator<ArticleBase | null, void, unknown>;
}

export default (fetchFn: FetchFn): ArticleApi => {
	return {
		list: makeAsyncGenerator(async () => {
			return (await fetchFn<ArticleBase[]>('/api/articles/') || []);
		}),
		get: makeAsyncGenerator(async (slug: string) => {
			return await fetchFn<ArticleBase>(`/api/articles/${slug}`);
		}),
		add: makeAsyncGenerator(async (data: Record<string, unknown>) => {
			return await fetchFn<ArticleBase>('/api/articles/create', {
				method: 'POST',
	  	        headers: {
		        	'Content-Type': 'application/json',
		        },
				body: JSON.stringify(data)
			});
		}),
		updateOne: makeAsyncGenerator(async (slug: string, data: Record<string, unknown>) => {
			return await fetchFn<ArticleBase>(`/api/articles/${slug}`, {
				method: 'PUT',
				headers: {
	        		'Content-Type': 'application/json',
	        	},
				body: JSON.stringify(data)
			});
		}),
		updateMany: async function* () {
			throw new Error('Not implemented');
		},
		markSeen: makeAsyncGenerator(async (data: Record<string, unknown>) => {
			return await fetchFn<ArticleBase>(`/api/articles/seen`, {
				method: 'POST',
	        	headers: {
	        		'Content-Type': 'application/json',
	        	},
				body: JSON.stringify(data)
			});
		}),
	}
}
