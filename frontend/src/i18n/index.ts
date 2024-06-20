import { profile } from '@/use/user'
import en from './en'
import de from './de'
import el from './el'

const languages: Record<string, Record<string, string>> = {
    en,
    de,
    el,
}

const currentLanguage = () => profile.interfaceLanguage || 'en'

export const supportedLanguages: Record<string, string> = {
    'en': 'English',
    'de': 'Deutsch',
    // 'fr': 'Français',
    // 'es': 'Español',
    // 'pt': 'Português',
    'el': 'Ελληνικά',  // Greek
    // 'pl': 'Polski',    // Polish
    // 'ru': 'Русский',   // Russian
}


const translate = (key: string): string => {
    const table = languages[currentLanguage()]
    if (!table) {
        console.error('Language not supported:', currentLanguage())
        return key
    }
    const translation = table[key]
    if (!translation) {
        console.warn('key not found with current language', currentLanguage(), key)
        return key
    }

    return translation
}

export default (key: string, ...args: (string | number)[]): string => {
    return args.reduce((text: string, arg, index) => text.replace(`$${index+1}`, `${arg}`), translate(key))
}
