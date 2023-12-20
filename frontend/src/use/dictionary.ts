import { watch } from 'vue';
import type { Ref } from 'vue';

import type { PartialWord, Word } from '@/types';
import type { DictionaryView, FilterFunction } from '@/dictionary/view';
import type { DictionaryCollection } from '@/dictionary/collection';

import createDictionaryStorage from '@/dictionary/storage';
import createDictionaryRequest from '@/dictionary/request';
import createDictionaryView from '@/dictionary/view';
import createDictionaryCollection from '@/dictionary/collection';

import useApi from './api';


export const useCustomDictionary = (words: PartialWord[] = [], filter: FilterFunction): DictionaryView => {
	const { fetchAuthorized } = useApi()
	const dictionaryRequest = createDictionaryRequest(fetchAuthorized)
	const dictionary = createDictionaryCollection(dictionaryRequest, words)

	return createDictionaryView(dictionary, filter)
}


let dictionary: DictionaryCollection | null = null
let isLoadingDictionary: Ref<boolean> | null = null
export const useDictionaryView = (filter: FilterFunction = x => !!x) => {
	if (!dictionary) {		
		const { fetchAuthorized, isLoading } = useApi()
		const dictionaryRequest = createDictionaryRequest(fetchAuthorized)
		const dictionaryStorage = createDictionaryStorage(dictionaryRequest, 'mainDictionary')
		
		isLoadingDictionary = isLoading;
		dictionary = createDictionaryCollection(dictionaryStorage);
		dictionary.load();
	}

	return {
		dictionary: createDictionaryView(dictionary, filter),
		isLoading: isLoadingDictionary!
	}
}
