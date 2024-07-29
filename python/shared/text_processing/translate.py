import re
from translate_shell.translate import translate
from datetime import datetime


def translate_single_word(word, source_language, target_language, language_collection=None):
    if language_collection is not None:
        # Check if the word exists in the collection
        existing_translation = language_collection.find_one(
            {
                'original': word,
                'source_language': source_language,
                'target_language': target_language,
            },
            {
                'translations': 1,
                '_id': 0
            }
        )

        if existing_translation:
            return existing_translation['translations'], True

    # If not found in the collection, use the translate function
    success = False
    try:
        translation_result = translate(word, source_lang=source_language, target_lang=target_language).results[0]
        success = True
    except Exception as e:
        # Code that runs if any other exception occurs
        print(f"Failed to translate word '{word}': {e}")
        translation_result = {
            'paraphrase': [word],
            'alternatives': []
        }

    primary = translation_result['paraphrase']
    alternatives = translation_result['alternatives']

    # Combine primary and alternatives into one list
    translations = [primary] + alternatives

    if success and language_collection is not None:
        # Store the new translation in the collection
        language_collection.insert_one({
            'original': word,
            'translations': translations,
            'origin': 'google',
            'source_language': source_language,
            'target_language': target_language,
            'translation_date': datetime.utcnow()
        })

    return translations, success
