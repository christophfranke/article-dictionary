from flask import request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from utils.mongo import get_collection
from .helpers import create_status_map, get_word_status


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
            'status': article['status'],
            'statistics': statistics
        }

        formatted_articles.append(formatted_article)

    return jsonify(formatted_articles)