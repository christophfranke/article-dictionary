from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from utils.mongo import get_collection

from .helpers import get_dictionary_entries


@login_required
def get_article(slug):
    collection = get_collection('articles')
    article = collection.find_one({'slug': slug, 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    return jsonify({
        'id': str(article['_id']),
        'title': article['title'],
        'content': article['content'],
        'slug': article['slug'],
        'words': article['words'],
        'createdAt': article['created_at'],
        'lastRead': article['last_read'],
        'status': article['status'],
        'dictionary': get_dictionary_entries(article['words'])
    })
