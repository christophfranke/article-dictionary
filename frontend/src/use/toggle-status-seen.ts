import type { DictionaryCollection } from '@/dictionary/collection';

export const useToggleStatusSeen = (dictionary: DictionaryCollection) => {
	const toggleStatusSeen = (word: string) => {
	  const original = word.toLowerCase();
	  dictionary.updateWord(original, { status: ['new', 'seen'].includes(dictionary.find(original)?.status || '') ? 'known' : 'seen' });
	};

	return toggleStatusSeen;
}