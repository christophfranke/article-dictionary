from collections import Counter
from datetime import datetime

from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word
from text_processing.extract import extract_words
from text_processing.dictionary import add_text
from bson import ObjectId


WORD_CLUSTER_UPDATE_LIMIT = 100


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

    # words_to_update = dictionary.count_documents(query)
    # print(f'\n\n\nUpdating cluster_id for {WORD_CLUSTER_UPDATE_LIMIT}/{words_to_update} words:\n')

    words = dictionary.find(query).limit(WORD_CLUSTER_UPDATE_LIMIT)

    for word in words:
        lemma = word.get('lemma')
        if word['original'] == lemma:
            leader = word
        else:
            leader = dictionary.find_one({'original': lemma, 'user_id': word['user_id']})
            if leader is not None:
                if leader['original'] != leader['lemma']:
                    new_leader = dictionary.find_one({'original': leader['lemma'], 'user_id': word['user_id']})
                    if new_leader is None:
                        dictionary.update_one({'_id': leader['_id']}, {'$set': {'lemma': leader['original'], 'cluster_id': leader['_id']}})
                        print(f'Updated lemma to prevent circular lemma dependency: {leader['lemma']} -> {leader['original']}.')
                    else:
                        leader = new_leader
                        if leader['original'] != leader['lemma']:
                            dictionary.update_one({'_id': leader['_id']}, {'$set': {'lemma': leader['original'], 'cluster_id': leader['_id']}})
                            print(f'Updated lemma to prevent circular lemma dependency: {leader['lemma']} -> {leader['original']}.')

        if leader is None:
            leader = {
                'original': lemma,
                'translations': [lemma],
                'status': word['status'],
                'last_viewed': None,
                'review_level': word['review_level'],
                'needs_retranslate': True,
                'needs_clustering': True,
                'translation_origin': None,
                'cluster_id': None,
                'frequency': 0,
                'source_language': word['source_language'],
                'target_language': word['target_language'],
                'user_id': word['user_id'],
                'lemma': lemma,
            }
            result = dictionary.insert_one(leader)
            leader['_id'] = result.inserted_id

            print(f"Inserted lemma {lemma} for {word.get('original')}, because it was not in the dictionary.")

        cluster_id = leader.get('_id')
        status = word.get('status', 'new')
        statuses = [doc['status'] for doc in dictionary.find({'cluster_id': cluster_id}, {'status': 1})]

        if 'known' in statuses or status == 'known':
            cluster_status = 'known'
        elif 'seen' in statuses or status == 'seen':
            cluster_status = 'seen'
        elif all(status == 'ignore' for status in statuses) and status == 'ignore':
            cluster_status = 'ignore'
        else:
            cluster_status = 'new'

        dictionary.update_one({'_id': word['_id']}, {'$set': {
            'needs_clustering': False,
            'cluster_id': leader.get('_id'),
            'status': cluster_status,
        }})

        cluster = get_collection('cluster')
        cluster_entry = cluster.update_one(
            {'_id': leader['_id']},
            {'$set': {
                'needs_recalculation': True
            }},
            upsert=True
        )

        cluster_size = dictionary.count_documents({'cluster_id': leader['_id']})
        print(f'Updated cluster_id: {word['original']} -> {lemma} (size: {cluster_size})')
