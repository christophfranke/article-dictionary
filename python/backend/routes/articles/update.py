from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

from utils.mongo import get_collection
from utils.casing import camel_to_snake
from text_processing.language import get_languages
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
        title = data['title']
        if article['title'] != title and collection.find_one({'title': title, 'user_id': ObjectId(current_user.id)}):
            return jsonify({'error': 'Title already taken'}), 409

    article_data = {camel_to_snake(key): data[key] for key in data if key in ['title', 'content', 'last_read', 'status']}


    if 'content' in article_data:
        content = article_data['content']
        article_data['words'] = extract_words(content)
        article_data['unique_words'] = get_unique_words(content)
        add_text(article_data['content'], current_user.id, get_collection('dictionary'), get_collection('users'))

    if 'title' in article_data:
        title = data['title']
        from_lang, src_lang = get_languages(get_collection('users'), current_user.id)
        article_data['slug'] = slugify(title, from_lang, src_lang)

    if 'status' in article_data:
        if article_data['status'] == 'seen':
            article_data['last_read'] = datetime.utcnow()
        else:
            article_data['reading_index'] = 0

        if article_data['status'] == 'read':
            article_data['last_read'] = datetime.utcnow()


    collection.update_one({'_id': article['_id']}, {'$set': article_data})
    updated_article = collection.find_one({'_id': article['_id']})

    if 'status' in article_data:
        if article_data['status'] == 'read':
            new_index = len(updated_article.get('words', []))
            old_index = updated_article.get('reading_index', 0)

            dictionary = get_collection('dictionary')
            for i in range(old_index, new_index):
                if i in article['words']:
                    word = article['words'][i]
                    dictionary.update_one({'original': word, user_id: ObjectId(current_user.id)}, {'$set': {
                        'last_viewed': datetime.utcnow(),
                    }})


    return serialize(updated_article, current_user.id), 200
