import re
from translate_shell.translate import translate
from datetime import datetime
import requests

GOOGLE_TRANSLATION = 'google'
GLOSBE_TRANSLATION = 'glosbe'
COMBINED_TRANSLATION = 'glosbe/google'


def translate_google(word, src_lang, target_lang):
    # print(f"Using translate_shell for Google Translate on {word}")
    try:
        translation_result = translate(word, source_lang=src_lang, target_lang=target_lang).results[0]
    except Exception as e:
        # Code that runs if any other exception occurs
        print(f"Google Translate failed to translate word '{word}': {e}")
        return []

    primary = translation_result['paraphrase']
    alternatives = translation_result['alternatives']

    # Combine primary and alternatives into one list
    return [primary] + alternatives


# URL and Headers for glosbe translation
url = "https://translator-api.glosbe.com/translateByLangWithScore?sourceLang=el&targetLang=de"
headers = {
    "User-Agent": "International Reader (https://international-reader; public@krito.de)",
    "Content-Type": "text/plain;charset=UTF-8",
    "Accept": "application/json",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "same-site",
    # "Sec-GPC": "1",
    # "Priority": "u=4",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}
confidence_threshold = -0.6


def translate_glosbe(word, src_lang, target_lang):
    try:
        response = requests.post(url, headers=headers, data=word)

        if response.status_code == 200:
            json_data = response.json()
            translation = json_data.get('translation')
            score = json_data.get('scores')[0]
            if score > confidence_threshold:
                print(f'Glosbe Translate {word} -> {translation} ({score})')
                return [translation]
            else:
                print(f'Dropped Glosbe Translate {word} -> {translation} ({score}), low confidence.')
                return []
        else:
            print(f"Request failed: {response.status_code} {response.text}")
            return []
    except Exception as e:
        # Code that runs if any other exception occurs
        print(f"Glosbe Translate failed to translate word '{word}': {e}")
        return []


def translate_single_word(word, src_lang, target_lang, language_collection=None):
    if language_collection is not None:
        # Check if the word exists in the collection
        existing_translation = language_collection.find_one(
            {
                'original': word,
                'source_language': src_lang,
                'target_language': target_lang,
            },
            {
                'translations': 1,
                'origin': 1,
                '_id': 0,
            }
        )

        if existing_translation and existing_translation['origin'] != 'google':
            print(f"Found word in cached translations: {word}")
            return existing_translation['translations'], True, existing_translation['origin']

    # If not found in the collection, use the translate function
    glosbe_results = translate_glosbe(word, src_lang, target_lang)
    google_results = translate_google(word, src_lang, target_lang)

    seen = set()
    translations = []
    for item in google_results + glosbe_results:
        if item not in seen:
            translations.append(item)
            seen.add(item)
    origin = COMBINED_TRANSLATION

    if len(translations) < 1:
        print(f'Could not translate {word}, no results')
        return [word], False, origin

    print(f'Translated {word} -> {translations}')

    if language_collection is not None:
        # Store the new translation in the collection
        language_collection.insert_one({
            'original': word,
            'translations': translations,
            'origin': origin,
            'source_language': src_lang,
            'target_language': target_lang,
            'translation_date': datetime.utcnow()
        })

    return translations, True, origin
