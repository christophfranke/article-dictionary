import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Ref } from 'vue';

import type { FilterFunction } from '@/articles/view';
import type { ArticleCollection } from '@/articles/collection';

import createArticleApi from '@/articles/api';
import createArticleView from '@/articles/view';
import createArticleStorage from '@/articles/storage';
import createArticleCollection from '@/articles/collection';
import createEmptyArticleView from '@/articles/empty-view';


import { redirectToLogin, default as useApi } from './api';
import { profile } from './user';


const articles: { [key: string]: ArticleCollection } = {}
let isLoadingArticles: Ref<boolean> | null = null
let isSendingArticles: Ref<boolean> | null = null
let errorMessageArticles: Ref<string | null> | null = null
export const useArticleView = (filter: FilterFunction = x => !!x) => {
    if (!profile.isLoggedIn || !profile.email) {
        const route = useRouter();
        const router = useRoute();
        redirectToLogin(router, route);

        return {
            isLoading: ref(false),
            isSending: ref(false),
            articles: createEmptyArticleView()
        }
    }

    const key = profile.email;

    if (!articles[key]) {		
        const { fetchAuthorized, isLoading, isSending, errorMessage } = useApi()
        const articleApi = createArticleApi(fetchAuthorized)
        const articleCollection = createArticleCollection(articleApi);
		
        isLoadingArticles = isLoading;
        isSendingArticles = isSending;
        errorMessageArticles = errorMessage;
        articles[key] = createArticleStorage(articleCollection, `${key}-articles`);
    }

    return {
        articles: createArticleView(articles[key], filter),
        isLoading: isLoadingArticles!,
        isSending: isSendingArticles!,
        errorMessage: errorMessageArticles!
    }
}
