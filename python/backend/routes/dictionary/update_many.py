from flask import jsonify, request
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId

from .helpers import serialize_many

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
        if 'translations' in data:
            word['needs_retranslate'] = False
            word['needs_clustering'] = True
        for key, value in update.items():
            word[key] = value
            dictionary_collection.replace_one({'_id': word['_id']}, word)

    return serialize_many(words)
