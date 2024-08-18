from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

from utils.mongo import get_collection

from .helpers import serialize, get_tokens


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
        tokens = get_tokens(article.get('tree', []))
        print(f'updating words for seen article {article.get("title")} ({old_index} - {new_index})')

        words_to_update = list(set([token['word'] for token in tokens[old_index:min(new_index, len(tokens))]]))

        if words_to_update:
            print(f'viewed words: {words_to_update}')
            dictionary.update_many(
                {
                    'original': {'$in': words_to_update},
                    'user_id': ObjectId(current_user.id),
                    'status': 'known'
                },
                {'$set': {
                    'last_viewed': datetime.utcnow(),
                }}
            )

    index = data.get('index', article.get('reading_index', 0))

    collection.update_one({'_id': article['_id']}, {'$set': {
        'last_read': datetime.utcnow(),
        'status': 'seen',
        'reading_index': index
    }})

    return jsonify({
        'id': id,
        'lastRead': datetime.utcnow(),
        'status': 'seen',
        'readingIndex': index,
    }), 200
