import { computed } from 'vue';
import type { DictionaryView } from './view';


export default (): DictionaryView => {
    return {
        find: () => undefined,
        findById: () => undefined,
        isVisible: () => false,
        items: computed(() => []),
        all: computed(() => []),
        setFilter: () => {},
        setOrder: () => {},
        discard: () => {},
        load: () => Promise.resolve(null),
        get: () => Promise.resolve(null),
        updateMany: () => Promise.resolve(null),
        updateOne: () => Promise.resolve(null),
        add: () => Promise.resolve(null),
        retranslate: () => Promise.resolve(null),
        rebuild: () => Promise.resolve(null),
        markSeen: () => Promise.resolve(null),
        detail: () => computed(() => undefined),
        getWord: () => Promise.resolve(null),
    };
}