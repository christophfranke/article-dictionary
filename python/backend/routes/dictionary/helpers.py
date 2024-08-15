from flask import jsonify
from utils.casing import camel_to_snake

known_level = 5


def select(word):
    return {
        'id': str(word['_id']),
        'clusterId': str(word.get('cluster_id', word['_id'])),
        'original': word.get('original', ''),
        'translations': word.get('translations', []),
        'status': word.get('status', 'new'),
        'frequency': word.get('frequency', 0),
        'lastViewed': word.get('last_viewed', None),
        'reviewLevel': word.get('review_level', known_level if word['status'] == 'known' else 0),
        'needsRetranslate': word.get('needs_retranslate'),
    }


def serialize(word):
    return jsonify(select(word))


def serialize_many(words):
    return jsonify([select(word) for word in words])


def update_word_data(word, data):
    if 'translations' in data:
        word['needs_retranslate'] = False
        word['translation_origin'] = 'user'

    if 'review_level' not in word:
        word['review_level'] = known_level if word['status'] == 'known' else 0

    # status levels:
    # 0: new
    # 1: seen
    # 2: seen
    # 3: seen
    # 4: known
    # 5: known
    if 'status' in data and 'review_level' not in data:
        review_level = word.get('review_level', 0)
        if data['status'] == 'new':
            word['review_level'] = 0
        if data['status'] == 'seen' and review_level < 1:
            word['review_level'] = 1
        if data['status'] == 'seen' and review_level > known_level - 1:
            word['review_level'] = known_level - 1
        if data['status'] == 'known' and review_level < known_level:
            word['review_level'] = known_level

    if 'review_level' in data and 'status' not in data:
        if data['review_level'] == 0:
            word['status'] = 'new'
        if data['review_level'] > 0 and data['review_level'] < known_level:
            word['status'] = 'seen'
        if data['review_level'] >= known_level:
            word['status'] = 'known'

    allowed_keys = [
        'original',
        'translations',
        'status',
        'frequency',
        'last_viewed',
        'review_level',
        'needs_retranslate',
        'needs_clustering',
        'cluster_id'
    ]
    for json_key, value in data.items():
        key = camel_to_snake(json_key)
        if key in allowed_keys:
            word[key] = value

    return word
