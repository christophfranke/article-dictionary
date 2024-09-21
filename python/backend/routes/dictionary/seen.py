from flask import jsonify, request
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime

from .helpers import serialize, update_word_data


@login_required
def seen_word(id):
    _id = ObjectId(id)

    dictionary_collection = get_collection('dictionary')

    word = dictionary_collection.find_one({'_id': _id, 'user_id': ObjectId(current_user.id)})

    if word is None:
        return jsonify({'error': f'Word not found: {id}'}), 404

    last_viewed = datetime.utcnow()
    old_status = word.get('status', 'new')
    if old_status == 'new':
        status = 'seen'
    else:
        status = old_status

    old_review_level = word.get('review_level', 0)
    if old_review_level == 0:
        review_level = 1
    else:
        review_level = old_review_level

    result = dictionary_collection.update_one({'_id': _id}, {
        '$set': {
            'last_viewed': last_viewed,
            'status': status,
            'review_level': review_level,
        }
    })

    if result.modified_count > 0:
        if word.get('cluster_id') is not None:
            if old_review_level != review_level or old_status != status:
                get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)

        return jsonify({
            'id': id,
            'lastViewed': last_viewed,
            'status': status,
            'reviewLevel': review_level,
        })

    return jsonify({
        'id': id
    })
