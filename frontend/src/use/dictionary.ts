import { ref } from 'vue';
import type { Ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'

import type { PartialWord, Word } from '@/types';
import type { DictionaryView, FilterFunction } from '@/dictionary/view';
import type { DictionaryCollection } from '@/dictionary/collection';

import createDictionaryStorage from '@/dictionary/storage';
import createDictionaryRequest from '@/dictionary/request';
import createDictionaryView from '@/dictionary/view';
import createDictionaryCollection from '@/dictionary/collection';
import createEmptyDictionaryView from '@/dictionary/empty-view';

import { profile } from './user';
import { default as useApi, redirectToLogin } from './api';


export const useCustomDictionary = (words: PartialWord[] = [], filter: FilterFunction): DictionaryView => {
	const { fetchAuthorized } = useApi()
	const dictionaryRequest = createDictionaryRequest(fetchAuthorized)
	const dictionary = createDictionaryCollection(dictionaryRequest, words)

	return createDictionaryView(dictionary, filter)
}


let dictionary: { [key:string]: DictionaryCollection } = {}
let isLoadingDictionary: Ref<boolean> | null = null
export const useDictionaryView = (filter: FilterFunction = x => !!x) => {
	if (!profile.isLoggedIn || !profile.email) {
		const route = useRouter();
		const router = useRoute();
		redirectToLogin(router, route);

		return {
			isLoading: ref(false),
			dictionary: createEmptyDictionaryView()
		}
	}

	const key = profile.email

	if (!dictionary[key]) {
		const { fetchAuthorized, isLoading } = useApi()
		const dictionaryRequest = createDictionaryRequest(fetchAuthorized)
		const dictionaryStorage = createDictionaryStorage(dictionaryRequest, `${key}-main-dictionary`)
		
		isLoadingDictionary = isLoading;
		dictionary[key] = createDictionaryCollection(dictionaryStorage);
	}

	return {
		dictionary: createDictionaryView(dictionary[key], filter),
		isLoading: isLoadingDictionary!
	}
}
