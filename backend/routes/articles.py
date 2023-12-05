# routes/articles.py
from flask import Blueprint, request, jsonify
from text_processing.extract import extract_words
from text_processing.dictionary import add_text
from utils.mongo import get_collection

articles = Blueprint('articles', __name__)

@articles.route('/')
def list_articles():
    try:
        # Retrieve all articles from the collection
        all_articles = get_collection('articles').find()

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

        articles_collection = get_collection('articles')

        # Check if the name is already taken
        if articles_collection.find_one({'name': name}):
            return jsonify({'error': 'Name already taken'}), 409

        # Insert new article into MongoDB
        new_article = {'name': name, 'content': content}
        result = articles_collection.insert_one(new_article)

        add_text(new_article['content'], get_collection('dictionary'))

        # Respond with the name of the newly created article and its URL
        response_data = {'name': name, 'url': f'/articles/{name}'}
        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@articles.route('/<name>')
def get_article(name):
    try:
        # Retrieve article from the collection
        article = get_collection('articles').find_one({'name': name})

        # Extract words from the article content
        article_words = extract_words(article['content'])

        # Retrieve dictionary entries for each word
        dictionary_entries = []
        dictionary_collection = get_collection('dictionary')

        for word in list(set([word.lower() for word in article_words])):
            dictionary_entry = dictionary_collection.find_one({'original': word}, { '_id': 0, 'language': 0 })
            if dictionary_entry:
                dictionary_entries.append(dictionary_entry)

        # Return article with additional 'dictionary' field as JSON
        return jsonify({
            'title': article['name'],
            'content': article['content'],
            'words': article_words,
            'dictionary': dictionary_entries,
        })

    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        return jsonify({'error': str(e)}), 500
