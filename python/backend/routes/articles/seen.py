from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

from utils.mongo import get_collection

from .helpers import serialize


@login_required
def seen_article():
    data = request.json
    id = data.get('id')
    index = data.get('index', 0)


    if not id:
        return jsonify({'error': 'Article id is required'}), 400

    collection = get_collection('articles')
    article = collection.find_one({'_id': ObjectId(id), 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    # update last read field
    collection.update_one({'_id': article['_id']}, {'$set': {
        'last_read': datetime.utcnow(),
        'status': 'seen',
        'reading_index': index
    }})

    article['status'] = 'seen'
    article['last_read'] = datetime.utcnow()
    return serialize(article, current_user.id), 200
