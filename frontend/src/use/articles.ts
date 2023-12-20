import type { Ref } from 'vue';

import type { ArticleBase } from '@/types';
import type { ArticleView, FilterFunction } from '@/articles/view';
import type { ArticleCollection } from '@/articles/collection';

import createArticleApi from '@/articles/api';
import createArticleView from '@/articles/view';
import createArticleStorage from '@/articles/storage';
import createArticleCollection from '@/articles/collection';

import useApi from './api';


let articles: ArticleCollection | null = null
let isLoadingArticles: Ref<boolean> | null = null
export const useArticleView = (filter: FilterFunction = x => !!x) => {
	if (!articles) {		
		const { fetchAuthorized, isLoading } = useApi()
		const articleApi = createArticleApi(fetchAuthorized)
		const articleStorage = createArticleStorage(articleApi, 'allArticles');
		
		isLoadingArticles = isLoading;
		articles = createArticleCollection(articleStorage);
		articles.load();
	}

	return {
		articles: createArticleView(articles, filter),
		isLoading: isLoadingArticles!
	}
}
