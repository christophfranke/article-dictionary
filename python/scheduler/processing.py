from collections import Counter
from pymongo import InsertOne, UpdateOne
from bson import ObjectId

from utils.mongo_external import get_collection
from nlp.analyze import process
from text_processing.dictionary import add_words
from text_processing.language import get_languages


def add_tokens(tokens, user_id, with_frequency=True):
    user_collection = get_collection('users')
    dictionary_collection = get_collection('dictionary')
    source_language, target_language = get_languages(user_collection, user_id)
    user_id_obj = ObjectId(user_id)

    # Prepare bulk operations
    bulk_insert_operations = []
    bulk_update_operations = []

    words = [token['word'] for token in tokens if not token['ignore']]
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
        freq = frequency[word] if with_frequency else 0
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

    print(f'Inserted {len(bulk_insert_operations)} and updated {len(bulk_update_operations)} words ({len(bulk_insert_operations) + len(bulk_update_operations)}/{len(unique_words)})')


def process_article():
    collection = get_collection('articles')
    article = collection.find_one({
        'needs_processing': True
    })

    if article is not None:
        user_id = ObjectId(article.get('user_id'))
        if user_id is None:
            print(f"Article has no user_id: {article.title}")
            return
        user = get_collection('users').find_one({'_id': user_id})
        if user is None:
            print(f"Article has invalid user_id: {article.title}, {user_id}")
            return

        src_lang, target_lang = user.get('source_language'), user.get('target_language')
        tokens = process(article['content'], src_lang, target_lang)

        add_tokens(tokens, user_id)

        collection.update_one({'_id': ObjectId(article.get('_id'))}, {
            '$set': {
                'tokens': tokens,
                'needs_processing': False,
            }
        })

        print(f"Processed article: {article['title']} ({src_lang} -> {target_lang})")
