from flask import jsonify
from utils.mongo import get_collection
from text_processing.dictionary import add_text
from flask_login import login_required, current_user
from bson import ObjectId


@login_required
def reset_dictionary():
    article_collection = get_collection('articles')

    articles_cursor = article_collection.find({'user_id': ObjectId(current_user.id)}, {'_id': 0, 'content': 1})

    dictionary_collection = get_collection('dictionary')

    for article in articles_cursor:
        content = article.get('content', '')
        add_text(content, ObjectId(current_user.id), dictionary_collection, get_collection('users'))

    return jsonify({'message': 'Reset successful'})
