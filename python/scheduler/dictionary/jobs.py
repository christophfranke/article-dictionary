from collections import Counter
from datetime import datetime

from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word
from text_processing.extract import extract_words
from text_processing.dictionary import add_text
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
            translations, success, origin = translate_single_word(
                word['original'],
                word['source_language'],
                word['target_language'],
                get_collection('translations')
            )

            # Update entry with translations
            word['translations'] = translations
            word['needs_retranslate'] = not success
            word['translation_origin'] = origin
            if word['original'] in translations:
                word['status'] = 'ignore'
            if word['cluster_id'] is not None:
                get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)

            if success:
                dictionary.replace_one({'_id': word['_id']}, word)
                print(f'Retranslated word {word["original"]}: {", ".join(map(str, translations))}')

    except Exception as e:
        print('Error retranslating word: ' + str(e))


def update_clusters():
    dictionary = get_collection('dictionary')

    query = {
        'needs_clustering': True,
        'lemma': {'$exists': True},
    }

    words = dictionary.find(query, {'original': 1, 'lemma': 1}).limit(10)

    for word in words:
        lemma = word.get('lemma')
        if word['original'] == lemma:
            leader = word
        else:
            leader = dictionary.find_one({'original': lemma}, {'_id': 1})

        if leader is None:
            print(f"Could not update word {word.get('original')}, lemma '{lemma}' is not in dictionary.")
            continue

        cluster_id = leader.get('_id')
        statuses = [doc['status'] for doc in dictionary.find({'cluster_id': cluster_id}, {'status': 1})]

        if 'known' in statuses:
            cluster_status = 'known'
        elif 'seen' in statuses:
            cluster_status = 'seen'
        elif all(status == 'ignore' for status in statuses):
            cluster_status = 'ignore'
        else:
            cluster_status = 'new'

        dictionary.update_one({'_id': word['_id']}, {'$set': {
            'needs_clustering': False,
            'cluster_id': leader.get('_id'),
            'status': cluster_status,
        }})

        cluster_size = dictionary.count_documents({'cluster_id': leader['_id']})
        print(f'Updated cluster: {word['original']} -> {lemma} (size: {cluster_size})')
