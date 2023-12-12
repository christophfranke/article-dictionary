from flask_login import current_user
from bson import ObjectId

from utils.mongo import get_collection


def slugify(title):
    return title.lower().replace(' ', '-')[:50]

def get_dictionary_entries(words):
    dictionary_collection = get_collection('dictionary')
    unique_words = list(set([word.lower() for word in words]))
    cursor = dictionary_collection.find(
        {'original': {'$in': unique_words}, 'user_id': ObjectId(current_user.id)},
        {'original': 1, 'translations': 1, 'frequency': 1, 'status': 1}
    )
    dictionary_entries = [
        {'id': str(entry['_id']), 'original': entry['original'], 'translations': entry['translations'],
         'frequency': entry['frequency'], 'status': entry['status']} for entry in cursor
    ]
    return dictionary_entries

def create_status_map(words):
    dictionary_collection = get_collection('dictionary')
    unique_words = list(set([word.lower() for word in words]))
    cursor = dictionary_collection.find(
        {'original': {'$in': unique_words}, 'user_id': ObjectId(current_user.id)},
        {'original': 1, 'status': 1}
    )
    status_map = {
        entry['original']: entry['status'] for entry in cursor
    }
    return status_map

def get_word_status(original, status_map):
    return status_map.get(original, 'unknown')