from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from utils.mongo import get_collection

from .helpers import serialize


@login_required
def get_article(slug):
    collection = get_collection('articles')
    article = collection.find_one({'slug': slug, 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    return serialize(article, current_user.id), 200
