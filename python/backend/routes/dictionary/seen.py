from flask import jsonify, request
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

from .helpers import serialize, update_word_data

@login_required
def seen_word(id):
    _id = ObjectId(id)

    dictionary_collection = get_collection('dictionary')

    word = dictionary_collection.find_one({'_id': _id, 'user_id': ObjectId(current_user.id)})

    if word is None:
        return jsonify({'error': f'Word not found: {id}'}), 404

    updated_word = word.copy()
    updated_word['last_viewed'] = datetime.utcnow()
    dictionary_collection.update_one({'_id': _id}, {
        '$set': {
            'last_viewed': updated_word['last_viewed'],
        }
    })

    return serialize(updated_word)
