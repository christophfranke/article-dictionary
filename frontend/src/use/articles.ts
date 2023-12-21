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
let errorMessageArticles: Ref<string | null> | null = null
export const useArticleView = (filter: FilterFunction = x => !!x) => {
	if (!articles) {		
		const { fetchAuthorized, isLoading, errorMessage } = useApi()
		const articleApi = createArticleApi(fetchAuthorized)
		// const articleStorage = createArticleStorage(articleApi, 'articles');
		
		isLoadingArticles = isLoading;
		errorMessageArticles = errorMessage;
		articles = createArticleCollection(articleApi);
		articles.load();
	}

	return {
		articles: createArticleView(articles, filter),
		isLoading: isLoadingArticles!,
		errorMessage: errorMessageArticles!
	}
}
