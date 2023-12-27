from text_processing.translate import translate_words
from text_processing.extract import extract_unique_words
from text_processing.language import get_languages
from bson import ObjectId  # Import ObjectId for converting user_id

def add_text(text, user_id, dictionary_collection, user_collection):
    words = extract_unique_words(text)
    add_words(words, user_id, dictionary_collection, user_collection)

def add_words(words, user_id, dictionary_collection, user_collection):
    new_words = []  # Array to collect yet-to-be-translated words

    source_language, target_language = get_languages(user_collection, user_id)

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

    # Iterate over the translations dictionary and add each word to the dictionary
    for original in new_words:
        new_word = {
            'original': original,
            'translations': [original],
            'status': 'new',
            'last_viewed': None,
            'review_level': 0,
            'needs_retranslate': True,
            'needs_recount': True,
            'needs_clustering': True,
            'translation_origin': None,
            'cluster_id': None,
            'frequency': 1,
            'source_language': source_language,
            'target_language': target_language,
            'user_id': ObjectId(user_id)
        }

        dictionary_collection.insert_one(new_word)
        print(f"Word '{new_word['original']}' added to the dictionary.")
