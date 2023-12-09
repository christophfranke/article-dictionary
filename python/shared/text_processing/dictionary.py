from text_processing.translate import translate_words
from text_processing.extract import extract_unique_words
from text_processing.language import get_languages
from bson import ObjectId  # Import ObjectId for converting user_id

def add_text(text, dictionary_collection, user_id):
    words = extract_unique_words(text)
    add_words(words, dictionary_collection, user_id)

def add_words(words, dictionary_collection, user_id):
    new_words = []  # Array to collect yet-to-be-translated words

    source_language, target_language = get_languages(user_id)

    for word in words:
        # Check if the word already exists in the dictionary
        existing_word = dictionary_collection.find_one({
            'original': word,
            'user_id': ObjectId(user_id),
            'source_language': source_language,
            'target_language': target_language,
        })

        if existing_word is None:
            # If the word is not in the dictionary, add it to the array
            new_words.append(word)
        else:
            dictionary_collection.update_one(
                {'_id': existing_word['_id']},
                {'$set': {'needs_recount': True}}
            )

    # Assuming translate function returns a dictionary
    try:
        translations = translate_words(new_words, source_language, target_language)
    except Exception as e:
        print(f'Error translating words: {e}')
        translations = {}

    if not set(new_words).issubset(translations.keys()):
        print(f'Translations do not cover all new words: {translations}')

    # Iterate over the translations dictionary and add each word to the dictionary
    for original_word, translation_possibilities in translations.items():
        trans = translation_possibilities or []
        primary = trans[0] if len(trans) > 0 else original_word
        status = 'new' if (len(trans) > 0 and original_word != primary) or len(trans) == 0 else 'ignore'
        new_word = {
            'original': original_word,
            'translations': [primary],
            'status': status,
            'needs_retranslate': True,
            'needs_recount': True,
            'frequency': 1,
            'source_language': source_language,
            'target_language': target_language,
            'user_id': ObjectId(user_id)
        }

        dictionary_collection.insert_one(new_word)
        print(f"Word '{new_word['original']}' added to the dictionary.")
