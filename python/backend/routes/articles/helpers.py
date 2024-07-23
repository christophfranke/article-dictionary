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


def create_status_map():
    dictionary = get_collection('dictionary')
    pipeline = [
        {
            '$match': {
                'user_id': ObjectId(current_user.id)
            }
        },
        {
            '$lookup': {
                'from': 'cluster',  # The collection to join
                'localField': 'cluster_id',  # The field from the `dictionary` collection
                'foreignField': '_id',  # The field from the `cluster` collection
                'as': 'cluster_data'  # The output array field
            }
        },
        {
            '$project': {
                'original': 1,
                'status': 1,
                'cluster_data': 1  # Include the joined data in the projection
            }
        }
    ]

    words = list(dictionary.aggregate(pipeline))
    status_map = {
        entry['original']: {
            'status': entry['status'],
            'cluster_status': entry['cluster_data'][0].get('status') if len(entry['cluster_data']) > 0 else entry['status']
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


def create_statistics(article):
    status_map = create_status_map()
    index = article.get('reading_index', 0)
    unread_words = article['words'][index:]

    return {
        'total': len([
            word for word in article['words']
            if get_word_status(word, status_map) != 'ignore'
        ]),
        'total_unread': len(unread_words),
        'new': {
            'words': len([
                word for word in article['words']
                if not get_word_status(word, status_map)
                or get_word_status(word, status_map) == 'new'
            ]),
        },
        'seen': {
            'words': len([
                word for word in article['words']
                if get_word_status(word, status_map) == 'seen'
            ]),
        },
        'known': {
            'words': len([
                word for word in article['words']
                if get_word_status(word, status_map) == 'known'
            ]),
        }
    }


def serialize(article, user_id):
    tokens = [token for token in article.get('tokens', []) if not token['ignore']]
    needs_processing = article.get('needs_processing', True)
    return jsonify({
        'id': str(article['_id']),
        'title': article['title'],
        'content': article['content'],
        'excerpt': article['content'][:150],
        'owned': article['owner_id'] == ObjectId(user_id),
        'privacy': article['privacy'],
        'slug': article['slug'],
        'createdAt': article['created_at'],
        'lastRead': article['last_read'],
        'status': article['status'],
        'readingIndex': article.get('reading_index', 0),
        'statistics': create_statistics(article),
        'tokens': tokens,
        'needs_processing': needs_processing
    }), 202 if needs_processing else 200
