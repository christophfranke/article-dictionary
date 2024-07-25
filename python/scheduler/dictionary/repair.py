from collections import Counter
from datetime import datetime

from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word
from text_processing.extract import extract_words
from text_processing.dictionary import add_to_cluster, add_text
from bson import ObjectId


def remove_no_original():
    dictionary = get_collection('dictionary')

    # Find word that meets the specified criteria
    query = {
        'original': {'$exists': False},  # Document must have the 'original' field
    }
    word = dictionary.find_one(query)

    if word:
        dictionary.delete_one({'_id': word['_id']})
        if word['cluster_id'] is not None:
            get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)
        print('Removed word: ' + word + ', had no original field')


def remove_invalid_src_or_target():
    collection = get_collection('dictionary')

    query = {
        '$or': [
            {'source_language': {'$exists': False}},
            {'target_language': {'$exists': False}},
            {'$expr': {'$eq': ['$source_language', '$target_language']}}
        ]
    }

    word = collection.find_one(query)
    if word:
        dictionary.delete_one({'_id': word['_id']})
        if word['cluster_id'] is not None:
            get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)
        print('Removed word: ' + word + ', source_language/target_language was incorrectly set')


def remove_duplicates():
    collection = get_collection('dictionary')

    pipeline = [
        {
            '$match': {
                'original': {'$exists': True},
                'source_language': {'$exists': True},
                'target_language': {'$exists': True},
                'user_id': {'$exists': True}
            }
        },
        {
            '$group': {
                '_id': {
                    'original': '$original',
                    'source_language': '$source_language',
                    'target_language': '$target_language',
                    'user_id': '$user_id'
                },
                'count': {'$sum': 1},
                'docs': {'$push': '$_id'}
            }
        },
        {
            '$match': {
                'count': {'$gt': 1}
            }
        },
        {
            '$project': {
                'docs': 1
            }
        }
    ]

    duplicate_groups = list(collection.aggregate(pipeline))

    for group in duplicate_groups:
        docs = group['docs']
        # Keep one document and remove the rest
        for duplicate_id in docs[1:]:
            duplicate_word = collection.find_one({'_id': duplicate_id})
            collection.delete_one({'_id': duplicate_id})
            print('Removed duplicate word: ' + duplicate_word['original'] + ' lang: ' + duplicate_word['source_language'] + ' -> ' + duplicate_word['target_language'])

    if not duplicate_groups:
        print('No duplicates found.')


def add_cluster_id():
    dictionary = get_collection('dictionary')

    query = {
        '$and': [
            {
                '$or': [
                    {'needs_clustering': {'$exists': False}},
                    {'needs_clustering': True}
                ]
            },
            {
                '$or': [
                    {'cluster_id': {'$exists': False}},
                    {'cluster_id': None}
                ]
            }
        ]
    }

    words = dictionary.find(query)

    for word in words:
        word['cluster_id'] = word['_id']
        word['needs_clustering'] = True
        dictionary.replace_one({'_id': word['_id']}, word)
        print('Added cluster_id to word: ' + word['original'])


def reset_clusters():
    dictionary = get_collection('dictionary')
    cluster = get_collection('cluster')
    cluster.delete_many({})

    words = dictionary.find()

    for word in words:
        dictionary.update_one({'_id': word['_id']}, {
            '$set': {
                'needs_clustering': True,
                'cluster_id': word['_id']
            }
        })
    print('Reset clusters')


def add_review_level_and_last_reviewed():
    dictionary = get_collection('dictionary')

    query = {
        'review_level': {'$exists': False},
        'last_viewed': {'$exists': False},
    }

    words = dictionary.find(query)

    for word in words:
        review_level = 0
        if word['status'] == 'seen':
            review_level = 1
        elif word['status'] == 'known':
            review_level = 4
        word['review_level'] = review_level
        word['last_viewed'] = datetime.now() if review_level > 0 else None
        dictionary.replace_one({'_id': word['_id']}, word)
        print('Added review_level and last_viewed to word: ' + word['original'])


def add_translation_origin():
    dictionary = get_collection('dictionary')

    query = {
        'translation_origin': {'$exists': False},
    }

    words = dictionary.find(query)

    for word in words:
        word['translation_origin'] = 'google'
        dictionary.replace_one({'_id': word['_id']}, word)
        print('Added translation_origin to word: ' + word['original'])
