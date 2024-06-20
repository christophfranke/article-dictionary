import en from './en'
import de from './de'

const languages = {
    en,
    de
}

const currentLanguage = 'de'

export const supportedLanguages = {
    'en': 'English',
    'de': 'Deutsch',
}


const translate = (key: string): string => {
    const table = languages[currentLanguage]
    if (!table) {
        console.error('Language not supported:', currentLanguage)
        return key
    }
    const translation = table[key]
    if (!translation) {
        console.warn('key not found with current language', currentLanguage, key)
        return key
    }

    return translation
}

export default (key: string, ...args: (string | number)[]): string => {
    return args.reduce((text: string, arg, index) => text.replace(`$${index+1}`, `${arg}`), translate(key))
}
