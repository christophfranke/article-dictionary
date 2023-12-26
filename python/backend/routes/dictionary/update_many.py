from flask import jsonify, request
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId

from .helpers import serialize_many, update_word_data

@login_required
def update_many():
    dictionary_collection = get_collection('dictionary')

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    ids = [ObjectId(id) for id in data.get('ids', [])]
    update = data.get('update', {})

    if not ids:
        return jsonify({'error': 'No ids provided for update'}), 400

    if not update:
        return jsonify({'error': 'No update provided for update'}), 400

    words = list(dictionary_collection.find({'_id': {'$in': ids}, 'user_id': ObjectId(current_user.id)}))

    for word in words:
        new_word = update_word_data(word, update)
        dictionary_collection.replace_one({'_id': new_word['_id']}, new_word)
        if new_word['cluster_id'] is not None:
            get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)

    return serialize_many(words)
