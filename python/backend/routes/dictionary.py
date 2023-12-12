from flask import Blueprint, jsonify, request
from utils.mongo import get_collection, drop_collection
from text_processing.dictionary import add_text, add_words
from text_processing.translate import translate_single_word
from text_processing.language import get_languages
from flask_login import login_required, current_user
from bson import ObjectId

dictionary = Blueprint('dictionary', __name__)

def get_user_id():
    return ObjectId(current_user.id)

@dictionary.route('/')
@login_required
def list_words():
    dictionary_collection = get_collection('dictionary')

    words_cursor = dictionary_collection.find({'user_id': get_user_id()}, {'_id': 1, 'original': 1, 'translations': 1, 'frequency': 1, 'status': 1})

    words_list = list(words_cursor)

    for word in words_list:
        word['id'] = str(word.pop('_id'))

    return jsonify(words_list)

@dictionary.route('/reset', methods=['POST'])
@login_required
def reset_dictionary():
    article_collection = get_collection('articles')

    articles_cursor = article_collection.find({'user_id': get_user_id()}, {'_id': 0, 'content': 1})

    dictionary_collection = get_collection('dictionary')

    for article in articles_cursor:
        content = article.get('content', '')
        add_text(content, get_user_id(), dictionary_collection, get_collection('users'))

    return jsonify({'message': 'Reset successful'})

@dictionary.route('/update/<id>', methods=['PUT'])
@login_required
def update_word(id):
    _id = ObjectId(id)

    dictionary_collection = get_collection('dictionary')

    word = dictionary_collection.find_one({'_id': _id, 'user_id': get_user_id()})

    if word is None:
        return jsonify({'error': f'Word not found: {id}'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    if 'translations' in data:
        word['needs_retranslate'] = False

    for key, value in data.items():
        word[key] = value

    dictionary_collection.replace_one({'_id': _id}, word)

    updated_word = dictionary_collection.find_one({'_id': _id})
    updated_word['id'] = str(updated_word.pop('_id'))
    updated_word.pop('user_id')
    return jsonify(updated_word)

@dictionary.route('/update/', methods=['PUT'])
@login_required
def update_many():
    dictionary_collection = get_collection('dictionary')

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    ids = [ObjectId(id) for id in data.get('ids', [])]
    update = data.get('update', {})

    if not ids:
        return jsonify({'error': 'No ids provided for update'}), 400

    if not update:
        return jsonify({'error': 'No update provided for update'}), 400

    words = list(dictionary_collection.find({'_id': {'$in': ids}, 'user_id': get_user_id()}))

    for word in words:
        if 'translations' in data:
            word['needs_retranslate'] = False
        for key, value in update.items():
            word[key] = value
            dictionary_collection.replace_one({'_id': word['_id']}, word)

    for word in words:
        word['id'] = str(word.pop('_id'))
        word.pop('user_id')
    return jsonify(words)

@dictionary.route('/retranslate/<original>', methods=['POST'])
@login_required
def retranslate(original):
    dictionary_collection = get_collection('dictionary')

    word = dictionary_collection.find_one({'original': original, 'user_id': get_user_id()})

    if word is None:
        return jsonify({'error': f'Word not found: {original}'}), 404

    source_language, target_language = get_languages(get_collection('users'), get_user_id())
    word['translations'] = translate_single_word(original, source_language, target_language)
    word['needs_retranslate'] = False

    dictionary_collection.replace_one({'original': original, 'user_id': get_user_id()}, word)

    updated_word = dictionary_collection.find_one({'original': original, 'user_id': get_user_id()})
    updated_word['id'] = str(updated_word.pop('_id'))
    updated_word.pop('user_id')
    return jsonify(updated_word)

@dictionary.route('/add', methods=['POST'])
@login_required
def add_word():
    dictionary_collection = get_collection('dictionary')

    data = request.get_json()
    original_word = data.get('original')

    if not original_word:
        return jsonify({'error': 'No original word provided for addition'}), 400

    existing_word = dictionary_collection.find_one({'original': original_word, 'user_id': get_user_id()})

    if existing_word:
        return jsonify({'error': f'Word already exists in the dictionary: {original_word}'}), 400

    add_words([original_word], get_user_id(), dictionary_collection, get_collection('users'))

    added_word = dictionary_collection.find_one({'original': original_word, 'user_id': get_user_id()})
    added_word['id'] = str(added_word.pop('_id'))
    added_word.pop('user_id')
    return jsonify(added_word)
