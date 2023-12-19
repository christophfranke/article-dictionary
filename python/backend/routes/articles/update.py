from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from utils.mongo import get_collection
from utils.casing import camel_to_snake
from text_processing.extract import extract_words, get_unique_words
from text_processing.dictionary import add_text
from text_processing.characters import slugify

from .helpers import serialize


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
        article_data['unique_words'] = get_unique_words(content)
        add_text(article_data['content'], current_user.id, get_collection('dictionary'), get_collection('users'))

    if 'title' in article_data:
        article_data['slug'] = slugify(title)

    if 'status' in article_data:
        if article_data['status'] == 'seen':
            article_data['last_read'] = datetime.utcnow()
        else:
            article_data['reading_index'] = 0


    collection.update_one({'_id': article['_id']}, {'$set': article_data})

    updated_article = collection.find_one({'_id': article['_id']})
    return serialize(updated_article, current_user.id), 200
