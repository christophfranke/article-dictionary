from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId

from text_processing.extract import extract_words
from text_processing.dictionary import add_text
from text_processing.language import get_languages
from utils.mongo import get_collection
from flask_login import login_required, current_user

articles = Blueprint('articles', __name__)

def slugify(title):
    return title.lower().replace(' ', '-')[:50]

def get_dictionary_entries(words):
    dictionary_collection = get_collection('dictionary')
    unique_words = list(set([word.lower() for word in words]))
    cursor = dictionary_collection.find(
        {'original': {'$in': unique_words}, 'user_id': ObjectId(current_user.id)},
        {'original': 1, 'translations': 1, 'frequency': 1, 'status': 1}
    )
    dictionary_entries = [
        {'id': str(entry['_id']), 'original': entry['original'], 'translations': entry['translations'],
         'frequency': entry['frequency'], 'status': entry['status']} for entry in cursor
    ]
    return dictionary_entries

def create_status_map(words):
    dictionary_collection = get_collection('dictionary')
    unique_words = list(set([word.lower() for word in words]))
    cursor = dictionary_collection.find(
        {'original': {'$in': unique_words}, 'user_id': ObjectId(current_user.id)},
        {'original': 1, 'status': 1}
    )
    status_map = {
        entry['original']: entry['status'] for entry in cursor
    }
    return status_map

def get_word_status(original, status_map):
    return status_map.get(original, 'unknown')

@articles.route('/')
@login_required
def list_articles():
    articles_collection = get_collection('articles')
    all_articles = articles_collection.find({'user_id': ObjectId(current_user.id)})

    formatted_articles = []

    for article in all_articles:
        status_map = create_status_map(article['words'])
        statistics = {
            'total': len(article['words']),
            'new': len([word for word in article['words'] if get_word_status(word, status_map) == 'new']),
            'seen': len([word for word in article['words'] if get_word_status(word, status_map) == 'seen']),
            'known': len([word for word in article['words'] if get_word_status(word, status_map) == 'known']),
        }

        formatted_article = {
            'id': str(article['_id']),
            'title': article['title'],
            'excerpt': article['content'][:150],
            'slug': article['slug'],
            'createdAt': article['created_at'],
            'lastRead': article['last_read'],
            'statistics': statistics
        }

        formatted_articles.append(formatted_article)

    return jsonify(formatted_articles)

@articles.route('/create', methods=['POST'])
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
        'user_id': ObjectId(current_user.id)
    }

    result = articles_collection.insert_one(new_article)

    add_text(new_article['content'], get_collection('dictionary'), ObjectId(current_user.id))

    new_article.pop('_id')
    new_article.pop('user_id')
    new_article['createdAt'] = new_article.pop('created_at')
    new_article['lastRead'] = new_article.pop('last_read')
    return jsonify(new_article), 201

@articles.route('/<slug>', methods=['GET'])
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
        'dictionary': get_dictionary_entries(article['words'])
    })

@articles.route('/seen', methods=['POST'])
@login_required
def read_article():
    data = request.json
    id = data.get('id')

    if not id:
        return jsonify({'error': 'Article id is required'}), 400

    collection = get_collection('articles')
    article = collection.find_one({'_id': ObjectId(id), 'user_id': ObjectId(current_user.id)})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    # update last read field
    collection.update_one({'_id': article['_id']}, {'$set': {'last_read': datetime.utcnow()}})

    return jsonify({'message': 'Article updated successfully'}), 200
