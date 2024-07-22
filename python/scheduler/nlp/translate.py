from argostranslate import package
from argostranslate import translate

# Retrieve and print available packages
packages = package.get_installed_packages()
print(f"Available packages: {packages}")


def package_available(src_lang, target_lang):
    """Check if a translation package for the given language pair is available."""
    for pkg in packages:
        if pkg.from_code == src_lang and pkg.to_code == target_lang:
            return True
    return False


def direct_translate(word, src_lang, target_lang):
    # 1. Check if package is available (every package has a .from_code and .to_code attribute)
    if not package_available(src_lang, target_lang):
        # 2. Return False if not available
        return False

    # 3. Use translate.translate(word, src_lang, target_lang) and return result string
    translation = translate.translate(word, src_lang, target_lang)
    return translation


def translate_to_english(word, src_lang):
    # 1. Check if package is available (every package has a .from_code and .to_code attribute)
    if not package_available(src_lang, 'en'):
        # 2. Return False if not available
        return False

    # 3. Use translate.translate(word, src_lang, 'en') and return result string
    translation = translate.translate(word, src_lang, 'en')
    return translation


def translate_from_english(word, target_lang):
    # 1. Check if package is available (every package has a .from_code and .to_code attribute)
    if not package_available('en', target_lang):
        # 2. Return False if not available
        return False

    # 3. Use translate.translate(word, 'en', target_lang) and return result string
    translation = translate.translate(word, 'en', target_lang)
    return translation


def translate_text(text, src_lang, target_lang):
    # 1. Try to translate using direct_translate, return result if not False
    translation = direct_translate(text, src_lang, target_lang)
    if translation:
        return translation

    # 2. If that does not work, try to translate to English and then from English, return result if not False
    translation_to_english = translate_to_english(text, src_lang)
    if translation_to_english:
        translation_from_english = translate_from_english(translation_to_english, target_lang)
        if translation_from_english:
            return translation_from_english

    # 3. If that does not work, return token.text
    return token.text


def translate_token(token, src_lang, target_lang):
    return translate_text(token.text, src_lang, target_lang)


def translate_entity(entity, src_lang, target_lang):
    return translate_text(entity.text, src_lang, target_lang)
