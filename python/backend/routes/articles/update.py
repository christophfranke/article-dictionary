from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

from utils.mongo import get_collection
from utils.casing import camel_to_snake
from text_processing.language import get_languages
from text_processing.extract import extract_words, get_unique_words
from text_processing.dictionary import add_words
from text_processing.characters import slugify

from .helpers import serialize

MAX_CONTENT_LENGTH = 50000


@login_required
def update_article(slug):
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    collection = get_collection('articles')
    article = collection.find_one({'slug': slug, 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    if 'content' in data and len(data.get('content')) > MAX_CONTENT_LENGTH:
        return jsonify({'error': f'Content too long. Keep it under {MAX_CONTENT_LENGTH} characters.'}), 413

    if 'title' in data:
        title = data['title']
        if article['title'] != title and collection.find_one({'title': title, 'user_id': ObjectId(current_user.id)}):
            return jsonify({'error': 'Title already taken'}), 409

    article_data = {camel_to_snake(key): data[key] for key in data if key in ['title', 'content', 'lastRead', 'status']}

    if 'content' in article_data:
        article_data['needs_processing'] = True
        article_data['reading_index'] = 0

    if 'title' in article_data:
        title = data['title']
        src_lang, target_lang = get_languages(get_collection('users'), current_user.id)
        article_data['slug'] = slugify(title, src_lang, target_lang)

    if 'status' in article_data:
        if article_data['status'] == 'seen':
            article_data['last_read'] = datetime.utcnow()
        else:
            article_data['reading_index'] = 0

        if article_data['status'] == 'read':
            article_data['last_read'] = datetime.utcnow()

    collection.update_one({'_id': ObjectId(article['_id'])}, {'$set': article_data})
    updated_article = collection.find_one({'_id': article['_id']})

    if 'status' in article_data:
        if article_data['status'] == 'read':
            new_index = len(updated_article.get('words', []))
            old_index = updated_article.get('reading_index', 0)

            dictionary = get_collection('dictionary')
            words = updated_article.get('words', [])
            for i in range(old_index, min(new_index, len(words))):
                word = words[i]
                dictionary.update_one({
                    'original': word,
                    'user_id': ObjectId(current_user.id),
                    'status': 'known'
                }, {'$set': {
                    'last_viewed': datetime.utcnow(),
                }})

    return serialize(updated_article, current_user.id), 200
