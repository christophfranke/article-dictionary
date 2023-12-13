from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

from utils.mongo import get_collection
from text_processing.extract import extract_words, get_unique_words
from text_processing.language import get_languages
from text_processing.dictionary import add_words

from .helpers import slugify, serialize

@login_required
def create_article():
    data = request.json

    articles_collection = get_collection('articles')

    article_id = data.get('id')
    if article_id:
        article_template = articles_collection.find_one({
            '_id': ObjectId(article_id),
            'privacy': 'public'
        })
        if not article_template:
            return jsonify({'error': f'Article not found: {article_id}'}), 404

        title = article_template.get('title')
        content = article_template.get('content')
        privacy = 'private'
        owner = article_template.get('user_id')
    else:
        title = data.get('title')
        content = data.get('content')
        privacy = data.get('privacy')
        owner = current_user.id

    if not title:
        return jsonify({'error': 'Title is a required field'}), 400

    if not content:
        return jsonify({'error': 'Content is a required field'}), 400

    if not privacy:
        return jsonify({'error': 'Privacy is a required field'}), 400


    if articles_collection.find_one({'title': title, 'user_id': ObjectId(current_user.id)}):
        return jsonify({'error': 'Title already taken'}), 409

    words = extract_words(content)
    unique_words = get_unique_words(words)

    source_language, _ = get_languages(get_collection('users'), current_user.id)

    new_article = {
        'title': title,
        'content': content,
        'privacy': privacy,
        'owner_id': ObjectId(owner),
        'slug': slugify(title),
        'words': words,
        'unique_words': unique_words,
        'language': source_language,
        'created_at': datetime.utcnow(),
        'last_read': datetime.utcnow(),
        'status': 'new',
        'user_id': ObjectId(current_user.id)
    }

    result = articles_collection.insert_one(new_article)

    add_words(unique_words, current_user.id, get_collection('dictionary'), get_collection('users'))

    return serialize(new_article, current_user.id), 201
