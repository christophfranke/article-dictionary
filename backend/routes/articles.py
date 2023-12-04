# routes/articles.py
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
language = 'greek'

articles = Blueprint('articles', __name__)

# Assuming you have a MongoDB client already set up
username = 'root'
password = 'example'
client = MongoClient(f'mongodb://{username}:{password}@mongodb:27017/')
db = client['dictionary_app_data']
articles_collection = db['articles']

@articles.route('/')
def list_articles():
    try:
        # Retrieve all articles from the collection
        all_articles = articles_collection.find()

        # Format articles for response
        formatted_articles = [
            {
                'id': str(article['_id']),
                'title': article['name'],
                'excerpt': article['content'][:150],  # Truncate content to 150 characters for excerpt
                'url': f'/articles/{article["name"]}',
            }
            for article in all_articles
        ]

        # Return formatted articles as JSON
        return jsonify(formatted_articles)

    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        return jsonify({'error': str(e)}), 500


@articles.route('/create', methods=['POST'])
def create_article():
    try:
        data = request.json
        name = data.get('name')
        content = data.get('content')

        if not name or not content:
            return jsonify({'error': 'Name and content are required fields'}), 400

        # Check if the name is already taken
        if articles_collection.find_one({'name': name}):
            return jsonify({'error': 'Name already taken'}), 409

        # Insert new article into MongoDB
        new_article = {'name': name, 'content': content}
        result = articles_collection.insert_one(new_article)

        # Respond with the name of the newly created article and its URL
        response_data = {'name': name, 'url': f'/articles/{name}'}
        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@articles.route('/<name>')
def get_article(name):
    try:
        # Retrieve article from the collection
        article = articles_collection.find_one({'name': name})

        words = wordpunct_tokenize(article['content'])

        # Return article as JSON
        return jsonify({
            'name': article['name'],
            'content': words,
        })

    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        return jsonify({'error': str(e)}), 500