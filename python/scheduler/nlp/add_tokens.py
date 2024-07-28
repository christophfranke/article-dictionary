from collections import Counter
from pymongo import InsertOne, UpdateOne
from bson import ObjectId

from utils.mongo_external import get_collection
from nlp.analyze import process
from text_processing.dictionary import add_words
from text_processing.language import get_languages


def add_tree(tree, user_id):
    tokens = get_tokens(tree)
    add_tokens(tokens, user_id)


def get_tokens(tree):
    result = []
    for elem in tree:
        elem_type = elem.get('type')
        if elem_type == 'SENTENCE':
            result.extend(get_tokens(elem['children']))
        elif elem_type == 'WORD':
            result.append(elem)
        elif elem_type == 'ENTITY':
            result.append(elem)
        else:
            print(f'Unknown type: {elem}')

    return result


def add_tokens(tokens, user_id):
    user_collection = get_collection('users')
    dictionary_collection = get_collection('dictionary')
    source_language, target_language = get_languages(user_collection, user_id)
    user_id_obj = ObjectId(user_id)

    # Prepare bulk operations
    bulk_insert_operations = []
    bulk_update_operations = []

    words = [token['word'] for token in tokens if not token.get('ignore', False)]
    frequency = Counter(words)
    unique_words = set(words)
    lemmata = {word: next(token['lemma'] for token in tokens if token['word'] == word) for word in unique_words}

    # Fetch existing words in a single query
    existing_words = dictionary_collection.find({
        'original': {'$in': list(unique_words)},
        'user_id': user_id_obj,
        'source_language': source_language,
        'target_language': target_language,
    })

    # Create a set of existing words for quick lookup
    existing_words_set = set([word['original'] for word in existing_words])

    for word in unique_words:
        freq = frequency[word]
        if word not in existing_words_set:
            # If the word is not in the dictionary, prepare a bulk insert operation
            new_word = {
                'original': word,
                'translations': [word],
                'status': 'new',
                'last_viewed': None,
                'review_level': 0,
                'needs_retranslate': True,
                'needs_clustering': True,
                'translation_origin': None,
                'cluster_id': None,
                'frequency': freq,
                'source_language': source_language,
                'target_language': target_language,
                'user_id': user_id_obj,
                'lemma': lemmata[word],
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
                    {
                        '$inc': {'frequency': freq},
                        '$set': {'lemma': lemmata[word]},
                    }
                )
            )

    # Execute bulk insert operations
    if len(bulk_insert_operations) > 0:
        dictionary_collection.bulk_write(bulk_insert_operations)

    # Execute bulk update operations
    if len(bulk_update_operations) > 0:
        dictionary_collection.bulk_write(bulk_update_operations)

    bulk_lemmata_inserts = []

    unique_lemmata = list(set(lemmata.values()))
    existing_lemmata = dictionary_collection.find({
        'original': {'$in': unique_lemmata},
        'user_id': user_id_obj,
        'source_language': source_language,
        'target_language': target_language,
    })
    existing_lemmata_set = set([word['original'] for word in existing_lemmata])

    for lemma in unique_lemmata:
        if lemma not in existing_lemmata_set:
            # If the word is not in the dictionary, prepare a bulk insert operation
            new_word = {
                'original': lemma,
                'translations': [lemma],
                'status': 'new',
                'last_viewed': None,
                'review_level': 0,
                'needs_retranslate': True,
                'needs_clustering': True,
                'translation_origin': None,
                'cluster_id': None,
                'frequency': 0,
                'source_language': source_language,
                'target_language': target_language,
                'user_id': user_id_obj,
                'lemma': lemma,
            }

            bulk_lemmata_inserts.append(InsertOne(new_word))

    # Execute bulk insert operations
    if len(bulk_lemmata_inserts) > 0:
        dictionary_collection.bulk_write(bulk_lemmata_inserts)

    print(f'Inserted {len(bulk_insert_operations)} and updated {len(bulk_update_operations)} words, addded {len(bulk_lemmata_inserts)} lemmata ({len(bulk_insert_operations) + len(bulk_update_operations) + len(bulk_lemmata_inserts)}/{len(unique_words)})')
