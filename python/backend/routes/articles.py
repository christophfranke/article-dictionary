# routes/articles.py
from flask import Blueprint, request, jsonify
from text_processing.extract import extract_words
from text_processing.dictionary import add_text
from utils.mongo import get_collection

articles = Blueprint('articles', __name__)

def slugify(title):
    return title.lower().replace(' ', '-')[:50]

@articles.route('/')
def list_articles():
    # Retrieve all articles from the collection
    all_articles = get_collection('articles').find()

    # Format articles for response
    formatted_articles = [
        {
            'id': str(article['_id']),
            'title': article['title'],
            'excerpt': article['content'][:150],  # Truncate content to 150 characters for excerpt
            'slug': article['slug'],
        }
        for article in all_articles
    ]

    # Return formatted articles as JSON
    return jsonify(formatted_articles)


@articles.route('/create', methods=['POST'])
def create_article():
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required fields'}), 400

    articles_collection = get_collection('articles')

    # Check if the name is already taken
    if articles_collection.find_one({'title': title}):
        return jsonify({'error': 'Title already taken'}), 409

    # Insert new article into MongoDB
    new_article = {
        'title': title,
        'content': content,
        'slug': slugify(title),
    }

    result = articles_collection.insert_one(new_article)

    add_text(new_article['content'], get_collection('dictionary'))

    # Respond with the name of the newly created article and its URL
    new_article.pop('_id')
    return jsonify(new_article), 201

@articles.route('/<slug>', methods=['GET'])
def get_article(slug):
    # Retrieve article from the collection
    article = get_collection('articles').find_one({'slug': slug})

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    # Extract words from the article content
    article_words = extract_words(article['content'])

    # Retrieve dictionary entries for each word
    dictionary_entries = []
    dictionary_collection = get_collection('dictionary')


    for word in list(set([word.lower() for word in article_words])):
        dictionary_entry = dictionary_collection.find_one({'original': word}, { '_id': 1, 'language': 0 })
        if dictionary_entry:
            dictionary_entry['id'] = str(dictionary_entry.pop('_id'))
            dictionary_entries.append(dictionary_entry)

    # Return article with additional 'dictionary' field as JSON
    return jsonify({
        'title': article['title'],
        'content': article['content'],
        'slug': article['slug'],
        'words': article_words,
        'dictionary': dictionary_entries,
    })
