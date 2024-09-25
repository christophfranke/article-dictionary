import { computed } from 'vue';
import type { ComputedRef } from 'vue';

import type { ArticleBase, ArticlePreview, ArticleDetail } from '@/types';
import type { ArticleCollection } from './collection';
import type { View } from '@/layers/view';
import createView from '@/layers/view';


export type FilterFunction = (x: ArticleBase) => boolean;
export type OrderFunction = (x: ArticleBase) => number;

export interface ArticleView extends View<ArticleBase, 'slug', 'slug'> {
  markSeen: (data: Record<string, unknown>) => Promise<void>;
  previews: ComputedRef<ArticlePreview[]>;
  detail: (slug: string) => ComputedRef<ArticleDetail | undefined>;
}

function isArticlePreview(article: ArticleBase): article is ArticlePreview {
    return (article as ArticlePreview).excerpt !== undefined &&
         (article as ArticlePreview).lastRead !== undefined &&
         (article as ArticlePreview).createdAt !== undefined &&
         (article as ArticlePreview).statistics !== undefined;
}

function isArticleDetail(article: ArticleBase): article is ArticleDetail {
    return (article as ArticleDetail).tokens !== undefined;
}


export default (collection: ArticleCollection, filterFn: FilterFunction = x => !!x, orderFn: OrderFunction | null = null): ArticleView => {
    const view = createView(collection, filterFn, orderFn)

    const previews = computed<ArticlePreview[]>(() => {
        return view.items.value.filter(isArticlePreview) as unknown as ArticlePreview[]
    })
    const detail = (slug: string): ComputedRef<ArticleDetail | undefined> => computed<ArticleDetail | undefined>(() => {
        const article = view.find(slug);
        if (article) {
            return isArticleDetail(article) ? article : undefined
        }

        return undefined
    });

    return {
        ...view,
        previews,
        detail,
        markSeen: collection.markSeen,
    }
}