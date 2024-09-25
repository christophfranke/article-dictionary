import { computed } from 'vue';
import type { ArticleView } from './view';


export default (): ArticleView => {
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
        markSeen: () => Promise.resolve(),
        previews: computed(() => []),
        detail: () => computed(() => undefined)
    };
}