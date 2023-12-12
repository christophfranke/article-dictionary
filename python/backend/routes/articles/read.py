from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from utils.mongo import get_collection


@login_required
def read_article():
    data = request.json
    id = data.get('id')

    if not id:
        return jsonify({'error': 'Article id is required'}), 400

    collection = get_collection('articles')
    article = collection.find_one({'_id': ObjectId(id), 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    # update last read field
    collection.update_one({'_id': article['_id']}, {'$set': {
        'last_read': datetime.utcnow(),
        'status': 'seen'
    }})

    return jsonify({'message': 'Article updated successfully'}), 200
