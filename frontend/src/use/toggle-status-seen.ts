import type { DictionaryView } from '@/dictionary/view';

export const useToggleStatusSeen = (dictionary: DictionaryView) => {
	const toggleStatusSeen = (params: { word: string }, event: MouseEvent) => {
		const word = params.word;
		const shiftKey = event.shiftKey || event.metaKey || event.ctrlKey;
	  const original = word;
	  const status = dictionary.find(original)?.status;
	  if (status) {	  	
		  if (['new', 'seen'].includes(status)) {
				dictionary.updateWord(original, { status: shiftKey ? 'ignore' : 'known' });
		  } else {
		  	dictionary.updateWord(original, { status: 'seen' });
		  }
	  }
	};

	return toggleStatusSeen;
}