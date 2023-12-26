from flask import jsonify
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId

from .helpers import serialize_many


@login_required
def list_words():
    dictionary_collection = get_collection('dictionary')

    words_cursor = dictionary_collection.find({'user_id': ObjectId(current_user.id)})

    words_list = list(words_cursor)
    return serialize_many(words_list)
