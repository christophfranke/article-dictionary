import type { WordDetail } from '@/types'


const wordCache: Record<string, WordDetail> = {}
const get = (key: string): WordDetail | null => {
    return wordCache[key] ?? null
}
const add = (key: string, word: WordDetail) => {
    wordCache[key] = word
}

export default () => {
    return {
        get,
        add
    }
}