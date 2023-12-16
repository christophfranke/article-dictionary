from flask import jsonify
from flask_login import current_user
from bson import ObjectId

from utils.mongo import get_collection


def get_dictionary_entries(unique_words):
    dictionary_collection = get_collection('dictionary')
    cursor = dictionary_collection.find(
        {'original': {'$in': unique_words}, 'user_id': ObjectId(current_user.id)},
        {'original': 1, 'translations': 1, 'frequency': 1, 'status': 1}
    )
    dictionary_entries = [
        {'id': str(entry['_id']), 'original': entry['original'], 'translations': entry['translations'],
         'frequency': entry['frequency'], 'status': entry['status']} for entry in cursor
    ]
    return dictionary_entries

def is_status_higher(old_status, new_status):
    if new_status == 'ignore':
        return False

    # new_status is at least new
    if old_status == 'new' or old_status == 'ignore':
        return True

    # old_status is at least seen
    if old_status == 'seen' and new_status == 'known':
        return True

    # old_status is known
    return False

def create_status_map(words):
    dictionary_collection = get_collection('dictionary')
    words = list(dictionary_collection.find(
        {'user_id': ObjectId(current_user.id)},
        {'original': 1, 'status': 1, '_id': 1, 'cluster_id': 1}
    ))
    status_map = {
        entry['_id']: {
            'original': entry['original'],
            'status': entry['status'],
        } for entry in words
    }

    return status_map

def get_word_status(original, status_map):
    word = status_map.get(original, None)
    if word:
        return word['status']

    return None

def get_cluster_status(original, status_map):
    word = status_map.get(original, None)
    if word:
        return word['cluster_status']

    return None


def serialize(article, user_id):
    return jsonify({
        'id': str(article['_id']),
        'title': article['title'],
        'content': article['content'],
        'owned': article['owner_id'] == ObjectId(user_id),
        'privacy': article['privacy'],
        'slug': article['slug'],
        'words': article['words'],
        'createdAt': article['created_at'],
        'lastRead': article['last_read'],
        'status': article['status'],
        'dictionary': get_dictionary_entries(article['unique_words'])
    })
