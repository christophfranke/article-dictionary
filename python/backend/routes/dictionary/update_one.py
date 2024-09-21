from flask import jsonify, request
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId

from .helpers import serialize, update_word_data


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

    word = update_word_data(word, data)

    dictionary_collection.replace_one({'_id': _id}, word)
    if word['cluster_id'] is not None:
        get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)

    updated_word = dictionary_collection.find_one({'_id': _id})
    return serialize(updated_word)
