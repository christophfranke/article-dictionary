from flask import jsonify
from utils.mongo import get_collection
from text_processing.translate import translate_single_word
from text_processing.language import get_languages
from flask_login import login_required, current_user
from bson import ObjectId

from .helpers import serialize

@login_required
def retranslate(id):
    dictionary_collection = get_collection('dictionary')

    word = dictionary_collection.find_one({'_id': ObjectId(id), 'user_id': ObjectId(current_user.id)})

    if word is None:
        return jsonify({'error': f'Word not found: {id}'}), 404

    source_language, target_language = get_languages(get_collection('users'), ObjectId(current_user.id))
    word['translations'] = translate_single_word(word['original'], source_language, target_language)
    word['needs_retranslate'] = False
    word['needs_clustering'] = True
    word['translation_origin'] = 'google'

    dictionary_collection.replace_one({'_id': ObjectId(id), 'user_id': ObjectId(current_user.id)}, word)

    updated_word = dictionary_collection.find_one({'_id': ObjectId(id), 'user_id': ObjectId(current_user.id)})
    return serialize(updated_word)
