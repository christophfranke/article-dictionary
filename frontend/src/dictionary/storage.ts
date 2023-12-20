import type { PartialWord } from '@/types';
import type { DictionaryApi } from './request';
import createStorage from '@/layers/storage';

export default (request: DictionaryApi, key: string): DictionaryApi => {
	const storage = createStorage(request, key);

	return {
		...request,
		...storage
	}
}
