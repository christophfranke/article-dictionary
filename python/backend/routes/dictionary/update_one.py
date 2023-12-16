from flask import jsonify, request
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId

from .helpers import serialize

@login_required
def update_word(id):
    _id = ObjectId(id)

    dictionary_collection = get_collection('dictionary')

    word = dictionary_collection.find_one({'_id': _id, 'user_id': ObjectId(current_user.id)})

    if word is None:
        return jsonify({'error': f'Word not found: {id}'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    if 'translations' in data:
        word['needs_retranslate'] = False
        word['needs_clustering'] = True

    for key, value in data.items():
        word[key] = value

    dictionary_collection.replace_one({'_id': _id}, word)

    updated_word = dictionary_collection.find_one({'_id': _id})
    return serialize(updated_word)
