from flask import Blueprint, jsonify
from utils.mongo import get_collection, drop_collection
from text_processing.dictionary import add_text
import sys

dictionary = Blueprint('dictionary', __name__)


@dictionary.route('/')
def list_words():
    try:
        dictionary_collection = get_collection('dictionary')

        # Retrieve all words from the dictionary_collection
        words_cursor = dictionary_collection.find({}, {'_id': 0, 'original': 1, 'translated': 1, 'status': 1})

        # Convert the cursor to a list of words
        words_list = list(words_cursor)

        # Return the list of words as JSON
        return jsonify(words_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error


@dictionary.route('/reset', methods=['POST'])
async def reset_dictionary():
    try:
        # Drop the dictionary collection
        drop_collection('dictionary')

        # Access the article collection
        article_collection = get_collection('articles')

        # Iterate through articles and call add_text function
        articles_cursor = article_collection.find({}, {'_id': 0, 'content': 1})

        dictionary_collection = get_collection('dictionary')

        for article in articles_cursor:
            content = article.get('content', '')
            await add_text(content, dictionary_collection)

        return jsonify({'message': 'Reset successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error
