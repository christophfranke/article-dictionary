from flask import jsonify
from utils.mongo import get_collection
from text_processing.translate import translate_single_word
from text_processing.language import get_languages
from flask_login import login_required, current_user
from bson import ObjectId


@login_required
def retranslate(original):
    dictionary_collection = get_collection('dictionary')

    word = dictionary_collection.find_one({'original': original, 'user_id': ObjectId(current_user.id)})

    if word is None:
        return jsonify({'error': f'Word not found: {original}'}), 404

    source_language, target_language = get_languages(get_collection('users'), ObjectId(current_user.id))
    word['translations'] = translate_single_word(original, source_language, target_language)
    word['needs_retranslate'] = False
    word['needs_clustering'] = True

    dictionary_collection.replace_one({'original': original, 'user_id': ObjectId(current_user.id)}, word)

    updated_word = dictionary_collection.find_one({'original': original, 'user_id': ObjectId(current_user.id)})
    updated_word['id'] = str(updated_word.pop('_id'))
    updated_word.pop('user_id')
    return jsonify(updated_word)
