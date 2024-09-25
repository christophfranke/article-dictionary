import type { DictionaryApi } from './request';
import type { PartialWord } from '@/types';
import type { Collection } from '@/layers/collection';
import createCollection from '@/layers/collection';

export interface DictionaryCollection extends Collection<PartialWord, 'original', 'id'> {
  retranslate: (original: string) => Promise<PartialWord | null>;
  rebuild: () => Promise<PartialWord[] | null>;
  markSeen: (id: string) => Promise<PartialWord | null>;
  getWord: (id: string) => Promise<PartialWord | null>;
}


export default (request: DictionaryApi, _words: PartialWord[] = []): DictionaryCollection => {
    const collection = createCollection<PartialWord, 'original', 'id'>(request, 'original', 'id');

    const retranslate = async (id: string): Promise<PartialWord | null> => {
        let result = null;
        for await (const retranslatedWord of request.retranslate(id)) {        
            if (retranslatedWord) {
                collection.updateLocal([retranslatedWord]);
                result = retranslatedWord;
            }
        }

        return result;
    };

    const rebuild = async (): Promise<PartialWord[] | null> => {
        for await (const _ of request.rebuild());
        return await collection.load();
    }

    const markSeen = async (id: string): Promise<PartialWord | null> => {
        let result = null;
        const word = collection.findById(id)
        const originalStatus = word?.status ?? null
        if (word?.status === 'new') {
            word.status = 'seen'
        }
        for await (const seenWord of request.markSeen(id)) {
            if (seenWord) {
                if (word && word?.status !== originalStatus) {
                    seenWord.status = word.status
                }

                collection.updateLocal([seenWord]);
                result = seenWord;
            }
        }

        if (word && originalStatus && !result) {
            word.status = originalStatus
        }
        return result;
    };

    const getWord = async (id: string): Promise<PartialWord | null> => {
        let result = null;
        for await (const word of request.getWord(id)) {
            if (word) {
                collection.updateLocal([word]);
                result = word;
            }
        }

        return result;
    }

    const updateOne = async (id: string, data: Record<string, unknown>): Promise<PartialWord | null> => {
        const word = collection.findById(id)
        const originalWord = word ? {
            ...word
        } : null
        if (word) {
            Object.assign(word, data)
        }
        const result = await collection.updateOne(id, data)
        if (word && originalWord && !result) {
            Object.assign(word, originalWord)
        }

        return result
    };

    return {
        ...collection,
        updateOne,
        markSeen,
        retranslate,
        rebuild,
        getWord,
    }
}
