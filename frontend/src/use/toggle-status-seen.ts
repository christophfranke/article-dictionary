import type { DictionaryView } from '@/dictionary/view';

export const useToggleStatusSeen = (dictionary: DictionaryView) => {
	const toggleStatusSeen = (params: { word: string }, event: MouseEvent) => {
		const shiftKey = event.shiftKey || event.metaKey || event.ctrlKey;
	  const original = params.word;
	  const word = dictionary.find(original);
	  const status = word?.status;
	  if (status) {	  	
		  if (['new', 'seen'].includes(status)) {
				dictionary.updateOne(word.id, { status: shiftKey ? 'ignore' : 'known' });
		  } else {
		  	dictionary.updateOne(word.id, { status: 'seen' });
		  }
	  }
	};

	return toggleStatusSeen;
}