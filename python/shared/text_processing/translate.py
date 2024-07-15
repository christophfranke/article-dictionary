import re
from translate_shell.translate import translate
from datetime import datetime


def chunk_list(input_list, chunk_size):
    """Chunks a list into smaller lists of a specified size."""
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def translate_single_word(word, source_language, target_language, language_collection=None):
    if language_collection is not None:
        # Check if the word exists in the collection
        existing_translation = language_collection.find_one(
            {
                'original': word,
                'source_language': source_language,
                'target_language': target_language
            },
            {
                'translations': 1,
                '_id': 0
            }
        )

        if existing_translation:
            return existing_translation['translations']

    # If not found in the collection, use the translate function
    try:
        translation_result = translate(word, source_lang=source_language, target_lang=target_language).results[0]
    except Exception as e:
        # Code that runs if any other exception occurs
        print(f"failed to translate {word}: {e}")

    primary = translation_result['paraphrase']
    alternatives = translation_result['alternatives']

    # Combine primary and alternatives into one list
    translations = [primary] + alternatives

    if language_collection is not None:
        # Store the new translation in the collection
        language_collection.insert_one({
            'original': word,
            'translations': translations,
            'origin': 'google',
            'source_language': source_language,
            'target_language': target_language,
            'translation_date': datetime.utcnow()
        })

    return translations


def translate_words(words, source_language, target_language, chunk_size=200):
    translations = {}

    if words:
        # Chunk the list of words to be translated into smaller lists
        word_chunks = chunk_list(words, chunk_size)

        # Translate each chunk of words
        for chunk in word_chunks:
            # Join the words in the chunk into a single string
            chunk_text = '.\n##\n'.join(chunk)

            # Translate the chunk
            translation_result = translate(
                chunk_text,
                source_lang=source_language,
                target_lang=target_language
            ).results[0]

            # Use regex to split the translations back into a list
            primary_chunk = re.split(r'.?\s*\#\#\s*', translation_result['paraphrase'])

            # Populate the translations dictionary with primary translations
            for original, translation in zip(chunk, primary_chunk):
                translations[original] = [translation.strip()]

    return translations
