import { useFetchAuthorized } from './api';
import createDictionaryRequest from '@/dictionary/request';
import createDictionaryCollection from '@/dictionary/collection';
import type { PartialWord } from '@/types';
import type { DictionaryCollection } from '@/dictionary/collection';

type FilterFunction = (x: PartialWord) => boolean;

export default (words: PartialWord[] = [], filter: FilterFunction): DictionaryCollection => {
	const fetchAuthorized = useFetchAuthorized()
	const dictionaryRequest = createDictionaryRequest(fetchAuthorized)
	const dictionary = createDictionaryCollection(dictionaryRequest, words, filter)

	return dictionary
}
