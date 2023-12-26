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

    if not id:
        return jsonify({'error': 'Article id is required'}), 400

    collection = get_collection('articles')
    article = collection.find_one({'_id': ObjectId(id), 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    if 'index' in data:
        dictionary = get_collection('dictionary')
        new_index = data.get('index') + 1
        old_index = article.get('reading_index', 0) + 1
        words = article.get('words', [])
        print(f'updating words for seen article {article.get('title')} ({old_index} - {new_index})')
        for i in range(old_index, min(new_index, len(words))):
            print(f'viewed word {i}:{words[i]}')
            word = words[i]
            dictionary.update_one({
                'original': word,
                'user_id': ObjectId(current_user.id),
                'status': 'known'
            }, {'$set': {
                'last_viewed': datetime.utcnow(),
            }})

    index = data.get('index', article.get('reading_index', 0))

    # update last read field
    collection.update_one({'_id': article['_id']}, {'$set': {
        'last_read': datetime.utcnow(),
        'status': 'seen',
        'reading_index': index
    }})

    article['status'] = 'seen'
    article['last_read'] = datetime.utcnow()
    article['reading_index'] = index
    return serialize(article, current_user.id), 200
