from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from utils.mongo import get_collection
from utils.casing import camel_to_snake
from text_processing.extract import extract_words
from text_processing.dictionary import add_text

from .helpers import slugify, get_dictionary_entries


@login_required
def update_article(slug):
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    collection = get_collection('articles')
    article = collection.find_one({'slug': slug, 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    if 'title' in data:
        if article['title'] != title and collection.find_one({'title': title, 'user_id': ObjectId(current_user.id)}):
            return jsonify({'error': 'Title already taken'}), 409

    article_data = {camel_to_snake(key): data[key] for key in data if key in ['title', 'content', 'last_read', 'status']}


    if 'content' in article_data:
        article_data['words'] = extract_words(content)
        add_text(article_data['content'], get_collection('dictionary'), ObjectId(current_user.id))

    if 'title' in article_data:
        article_data['slug'] = slugify(title)

    collection.update_one({'_id': article['_id']}, {'$set': article_data})

    updated_article = collection.find_one({'_id': article['_id']})
    return jsonify({
        'id': str(updated_article['_id']),
        'title': updated_article['title'],
        'content': updated_article['content'],
        'slug': updated_article['slug'],
        'words': updated_article['words'],
        'createdAt': updated_article['created_at'],
        'lastRead': updated_article['last_read'],
        'status': updated_article['status'],
        'dictionary': get_dictionary_entries(updated_article['words'])
    }), 200
