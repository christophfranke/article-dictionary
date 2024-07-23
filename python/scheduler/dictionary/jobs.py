from collections import Counter
from datetime import datetime

from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word
from text_processing.extract import extract_words
from text_processing.dictionary import add_to_cluster, add_text
from bson import ObjectId


def retranslate_word():
    try:
        dictionary = get_collection('dictionary')

        # Find word that meets the specified criteria
        query = {
            'original': {'$exists': True},  # Document must have the 'original' field
            'source_language': {'$exists': True},  # Document must have the 'source_language' field
            'target_language': {'$exists': True},  # Document must have the 'target_language' field
            'status': {'$ne': 'ignore'},  # 'status' is not set to 'ignore'
            '$or': [
                {'translations': {'$elemMatch': {'$eq': ''}}},  # Empty translation entry in the array
                {'translations': {'$elemMatch': {'$regex': '#'}}},   # Contains a hash in any translation
                {'needs_retranslate': True},  # Needs Review is set to True
            ]
        }
        word = dictionary.find_one(query)

        if word:
            # Translate
            translations = translate_single_word(
                word['original'],
                word['source_language'],
                word['target_language'],
                get_collection('translations')
            )

            # Update entry with translations
            word['translations'] = translations
            word['needs_retranslate'] = False
            word['needs_clustering'] = True
            word['translation_origin'] = 'google'
            if word['original'] in translations:
                word['status'] = 'ignore'
            dictionary.replace_one({'_id': word['_id']}, word)
            if word['cluster_id'] is not None:
                get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)

            print(f'Retranslated word {word["original"]}: {", ".join(map(str, translations))}')
    except Exception as e:
        print('Error retranslating word: ' + str(e))


def update_clusters():
    dictionary = get_collection('dictionary')

    query = {
        'needs_clustering': True,
        'needs_retranslate': False,
    }

    words = dictionary.find(query).limit(25)

    for word in words:
        word['needs_clustering'] = False
        add_to_cluster(get_collection, word)
        dictionary.update_one({'_id': word['_id']}, {'$set': {'needs_clustering': False }})
        updated_word = dictionary.find_one({'_id': word['_id']})
        leader_word = dictionary.find_one({'_id': updated_word['cluster_id']})
        cluster_size = dictionary.count_documents({'cluster_id': leader_word['_id']})
        print(f'Updated cluster: {updated_word['original']} -> {leader_word['original']} (size: {cluster_size})')
