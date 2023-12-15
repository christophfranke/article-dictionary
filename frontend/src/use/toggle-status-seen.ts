import type { DictionaryCollection } from '@/dictionary/collection';

export const useToggleStatusSeen = (dictionary: DictionaryCollection) => {
	const toggleStatusSeen = (word: string, event: MouseEvent) => {
		const shiftKey = event.shiftKey || event.metaKey || event.ctrlKey;
	  const original = word.toLowerCase();
	  const status = dictionary.find(original)?.status;
	  if (['new', 'seen'].includes(status)) {
			dictionary.updateWord(original, { status: shiftKey ? 'ignore' : 'known' });
	  } else {
	  	dictionary.updateWord(original, { status: 'seen' });
	  }
	};

	return toggleStatusSeen;
}