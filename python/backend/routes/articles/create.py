from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from utils.mongo import get_collection
from text_processing.extract import extract_words
from text_processing.language import get_languages
from text_processing.dictionary import add_text

from .helpers import slugify, get_dictionary_entries

@login_required
def create_article():
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required fields'}), 400

    articles_collection = get_collection('articles')

    if articles_collection.find_one({'title': title, 'user_id': ObjectId(current_user.id)}):
        return jsonify({'error': 'Title already taken'}), 409

    words = extract_words(content)

    source_language, _ = get_languages(current_user.id)

    new_article = {
        'title': title,
        'content': content,
        'slug': slugify(title),
        'words': words,
        'dictionary': get_dictionary_entries(words),
        'language': source_language,
        'created_at': datetime.utcnow(),
        'last_read': datetime.utcnow(),
        'status': 'new',
        'user_id': ObjectId(current_user.id)
    }

    result = articles_collection.insert_one(new_article)

    add_text(new_article['content'], get_collection('dictionary'), ObjectId(current_user.id))

    new_article.pop('_id')
    new_article.pop('user_id')
    new_article['createdAt'] = new_article.pop('created_at')
    new_article['lastRead'] = new_article.pop('last_read')
    return jsonify(new_article), 201