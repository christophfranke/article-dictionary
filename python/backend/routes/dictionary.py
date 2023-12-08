from flask import Blueprint, jsonify, request
from utils.mongo import get_collection, drop_collection
from text_processing.dictionary import add_text, add_words
from text_processing.translate import translate_single_word
from bson import ObjectId

dictionary = Blueprint('dictionary', __name__)

@dictionary.route('/')
def list_words():
    dictionary_collection = get_collection('dictionary')

    # Retrieve all words from the dictionary_collection
    words_cursor = dictionary_collection.find({}, { '_id': 1, 'original': 1, 'translations': 1, 'frequency': 1, 'status': 1 })

    # Convert the cursor to a list of words
    words_list = list(words_cursor)


    # Modify the _id field to id in each dictionary
    for word in words_list:
        word['id'] = str(word.pop('_id'))

    # Return the list of words as JSON
    return jsonify(words_list)

@dictionary.route('/reset', methods=['POST'])
def reset_dictionary():
    # Access the article collection
    article_collection = get_collection('articles')

    # Iterate through articles and call add_text function
    articles_cursor = article_collection.find({}, {'_id': 0, 'content': 1})

    dictionary_collection = get_collection('dictionary')

    for article in articles_cursor:
        content = article.get('content', '')
        add_text(content, dictionary_collection)

    return jsonify({'message': 'Reset successful'})

@dictionary.route('/update/<id>', methods=['PUT'])
def update_word(id):
    _id = ObjectId(id)

    # Retrieve the dictionary collection
    dictionary_collection = get_collection('dictionary')

    # Find the word in the dictionary
    word = dictionary_collection.find_one({'_id': _id})

    if word is None:
        return jsonify({'error': f'Word not found: {id}'}), 404

    # Update the word with the provided JSON data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    # Update fields based on the data
    for key, value in data.items():
        word[key] = value

    # Save the updated word back to the dictionary collection
    dictionary_collection.replace_one({'_id': _id}, word)

    # Retrieve the updated word from the dictionary
    updated_word = dictionary_collection.find_one({'_id': _id})
    updated_word['id'] = str(updated_word.pop('_id'))
    return jsonify(updated_word)


@dictionary.route('/update/', methods=['PUT'])
def update_many():
    # Retrieve the dictionary collection
    dictionary_collection = get_collection('dictionary')

    # Update the word with the provided JSON data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    ids = [ObjectId(id) for id in data.get('ids', [])]
    update = data.get('update', {})

    if not ids:
        return jsonify({'error': 'No ids provided for update'}), 400

    if not update:
        return jsonify({'error': 'No update provided for update'}), 400

    # Find the words in the dictionary
    words = list(dictionary_collection.find({'_id': {'$in': ids}}))

    # Update fields based on the data
    for word in words:
        for key, value in update.items():
            word[key] = value
            dictionary_collection.replace_one({'_id': word['_id']}, word)

    # Return the json words to the user
    for word in words:
        word['id'] = str(word.pop('_id'))
    return jsonify(words)


@dictionary.route('/retranslate/<original>', methods=['POST'])
def retranslate(original):
    # Retrieve the dictionary collection
    dictionary_collection = get_collection('dictionary')

    # Find the word in the dictionary
    word = dictionary_collection.find_one({'original': original})

    if word is None:
        return jsonify({'error': f'Word not found: {original}'}), 404

    # Retranslate the word
    word['translations'] = translate_single_word(original)

    # Has been retranslated manually, does not need automatic review
    word['needs_retranslate'] = False

    # Save the updated word back to the dictionary collection
    dictionary_collection.replace_one({'original': original}, word)

    # Retrieve the updated word from the dictionary
    updated_word = dictionary_collection.find_one({'original': original})
    updated_word['id'] = str(updated_word.pop('_id'))
    return jsonify(updated_word)


@dictionary.route('/add', methods=['POST'])
def add_word():
    # Retrieve the dictionary collection
    dictionary_collection = get_collection('dictionary')

    # Get the original word from the JSON data
    data = request.get_json()
    original_word = data.get('original')

    if not original_word:
        return jsonify({'error': 'No original word provided for addition'}), 400

    # Check if the word already exists in the dictionary
    existing_word = dictionary_collection.find_one({'original': original_word})

    if existing_word:
        return jsonify({'error': f'Word already exists in the dictionary: {original_word}'}), 400

    # Call add_words function to add the word to the dictionary
    add_words([original_word], dictionary_collection)

    # Retrieve the added word from the dictionary
    added_word = dictionary_collection.find_one({'original': original_word})
    added_word['id'] = str(added_word.pop('_id'))
    return jsonify(added_word)
