from bson import ObjectId  # Import ObjectId for converting user_id
from pymongo import InsertOne, UpdateOne
from text_processing.extract import extract_unique_words
from text_processing.language import get_languages


def add_text(text, user_id, dictionary_collection, user_collection):
    words = extract_unique_words(text)
    add_words(words, user_id, dictionary_collection, user_collection)


def add_words(words, user_id, dictionary_collection, user_collection):
    source_language, target_language = get_languages(user_collection, user_id)
    user_id_obj = ObjectId(user_id)

    # Prepare bulk operations
    bulk_insert_operations = []
    bulk_update_operations = []

    # Fetch existing words in a single query
    existing_words = dictionary_collection.find({
        'original': {'$in': words},
        'user_id': user_id_obj,
        'source_language': source_language,
        'target_language': target_language,
    })

    # Create a set of existing words for quick lookup
    existing_words_set = set([word['original'] for word in existing_words])

    for word in words:
        if word not in existing_words_set:
            # If the word is not in the dictionary, prepare a bulk insert operation
            new_word = {
                'original': word,
                'translations': [word],
                'status': 'new' if len(word) > 1 else 'ignore',
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
                'user_id': user_id_obj
            }

            bulk_insert_operations.append(InsertOne(new_word))
        else:
            # If the word exists, prepare a bulk update operation
            bulk_update_operations.append(
                UpdateOne(
                    {
                        'original': word,
                        'user_id': user_id_obj,
                        'source_language': source_language,
                        'target_language': target_language,
                    },
                    {'$set': {'needs_recount': True}}
                )
            )

    # Execute bulk insert operations
    if bulk_insert_operations:
        dictionary_collection.bulk_write(bulk_insert_operations)
        print(f"Inserted {len(bulk_insert_operations)} new words to the dictionary.")

    # Execute bulk update operations
    if bulk_update_operations:
        dictionary_collection.bulk_write(bulk_update_operations)
        print(f"Updated {len(bulk_update_operations)} existing words in the dictionary.")
