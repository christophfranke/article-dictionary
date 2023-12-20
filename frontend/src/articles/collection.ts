import type { ArticleApi } from './api';
import type { Collection } from '@/layers/collection';
import type { ArticleBase } from '@/types';
import createCollection from '@/layers/collection'

export interface ArticleCollection extends Collection<ArticleBase, 'slug', 'slug'> {
  markSeen: (data: Record<string, unknown>) => Promise<void>;
}

export default (api: ArticleApi): ArticleCollection => {
  const collection = createCollection(api, 'slug', 'slug');

  const markSeen = async (data: Record<string, unknown>): Promise<void> => {
    for await(const item of api.markSeen(data)) {
      if (item) {
        collection.updateLocal([item]);
      }
    }
  }

  return {
    ...collection,
    markSeen,
  }
}