# routes/articles.py
from flask import Blueprint, request, jsonify
from text_processing.extract import extract_words
from text_processing.dictionary import add_text
from utils.mongo import get_collection

articles = Blueprint('articles', __name__)

def slugify(title):
    return title.lower().replace(' ', '-')[:50]

def get_dictionary_entries(words):
    # Retrieve dictionary entries for each word
    dictionary_collection = get_collection('dictionary')

    # Convert words to lowercase and remove duplicates
    unique_words = list(set([word.lower() for word in words]))

    # Use a single query to fetch dictionary entries
    cursor = dictionary_collection.find(
        {'original': {'$in': unique_words}},
        {'original': 1, 'translations': 1, 'frequency': 1, 'status': 1}
    )

    # Transform cursor to list and add 'id' field
    dictionary_entries = [
        {'id': str(entry['_id']), 'original': entry['original'], 'translations': entry['translations'],
         'frequency': entry['frequency'], 'status': entry['status']} for entry in cursor
    ]

    return dictionary_entries

def create_status_map(words):
    # Retrieve dictionary entries for each word
    dictionary_collection = get_collection('dictionary')

    # Convert words to lowercase and remove duplicates
    unique_words = list(set([word.lower() for word in words]))

    # Use a single query to fetch dictionary entries
    cursor = dictionary_collection.find(
        {'original': {'$in': unique_words}},
        {'original': 1, 'status': 1}
    )

    # Transform cursor to a dictionary with word as key and status as value
    status_map = {
        entry['original']: entry['status'] for entry in cursor
    }

    return status_map


def get_word_status(original, status_map):
    return status_map.get(original, 'unknown')


@articles.route('/')
def list_articles():
    # Retrieve all articles from the collection
    all_articles = get_collection('articles').find()

    formatted_articles = []

    # Iterate through articles
    for article in all_articles:
        # Get dictionary entries for the article's words
        status_map = create_status_map(article['words'])

        # Calculate statistics for the article
        statistics = {
            'total': len(article['words']),
            'new': len([word for word in article['words'] if get_word_status(word, status_map) == 'new']),
            'seen': len([word for word in article['words'] if get_word_status(word, status_map) == 'seen']),
            'known': len([word for word in article['words'] if get_word_status(word, status_map) == 'known']),
        }

        # Format the article for response
        formatted_article = {
            'id': str(article['_id']),
            'title': article['title'],
            'excerpt': article['content'][:150],  # Truncate content to 150 characters for excerpt
            'slug': article['slug'],
            'statistics': statistics
        }

        formatted_articles.append(formatted_article)

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

    # This is only for debug purposes
    # if articles_collection.find_one({'title': title}):
    #     articles_collection.delete_one({'title': title})

    words = extract_words(content)

    # Insert new article into MongoDB
    new_article = {
        'title': title,
        'content': content,
        'slug': slugify(title),
        'words': words,
        'dictionary': get_dictionary_entries(words)
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


    # Return article with additional 'dictionary' field as JSON
    return jsonify({
        'title': article['title'],
        'content': article['content'],
        'slug': article['slug'],
        'words': article['words'],
        'dictionary': get_dictionary_entries(article['words'])
    })
