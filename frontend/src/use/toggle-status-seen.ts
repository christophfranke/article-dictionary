import type { Token } from '@/types';
import type { DictionaryView } from '@/dictionary/view';

export const useToggleStatusSeen = (dictionary: DictionaryView) => {
    const toggleStatusSeen = (params: { token: Token }, event: MouseEvent) => {
        const shiftKey = event.shiftKey || event.metaKey || event.ctrlKey;
        const original = params.token.word;
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