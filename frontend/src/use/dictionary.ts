import { watch } from 'vue';

import type { PartialWord } from '@/types';
import type { DictionaryView } from '@/dictionary/view';
import type { DictionaryCollection } from '@/dictionary/collection';

import createDictionaryRequest from '@/dictionary/request';
import createDictionaryView from '@/dictionary/view';
import createDictionaryCollection from '@/dictionary/collection';

import { useFetchAuthorized } from './api';


type FilterFunction = (x: PartialWord) => boolean;

export const useCustomDictionary = (words: PartialWord[] = [], filter: FilterFunction): DictionaryView => {
	const fetchAuthorized = useFetchAuthorized()
	const dictionaryRequest = createDictionaryRequest(fetchAuthorized)
	const dictionary = createDictionaryCollection(dictionaryRequest, words)

	return createDictionaryView(dictionary, filter)
}

let dictionary: DictionaryCollection | null = null
export const useDictionaryView = (filter: FilterFunction = x => !!x): DictionaryView => {
	if (!dictionary) {		
		const fetchAuthorized = useFetchAuthorized()
		const dictionaryRequest = createDictionaryRequest(fetchAuthorized)
		
		dictionary = createDictionaryCollection(dictionaryRequest, []);
		dictionary.load();
	}

	return createDictionaryView(dictionary, filter)
}
