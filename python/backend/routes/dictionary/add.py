from flask import jsonify, request
from utils.mongo import get_collection
from text_processing.dictionary import add_words
from flask_login import login_required, current_user
from bson import ObjectId

from .helpers import serialize


@login_required
def add_word():
    dictionary_collection = get_collection('dictionary')

    data = request.get_json()
    original_word = data.get('original')

    if not original_word:
        return jsonify({'error': 'No original word provided for addition'}), 400

    existing_word = dictionary_collection.find_one({'original': original_word, 'user_id': ObjectId(current_user.id)})

    if existing_word:
        return jsonify({'error': f'Word already exists in the dictionary: {original_word}'}), 400

    add_words([original_word], current_user.id, dictionary_collection, get_collection('users'))

    added_word = dictionary_collection.find_one({'original': original_word, 'user_id': ObjectId(current_user.id)})
    return serialize(added_word)