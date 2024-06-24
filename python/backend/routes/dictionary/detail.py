from flask_login import login_required, current_user
from flask import jsonify
from bson import ObjectId
from utils.mongo import get_collection
from text_processing.extract import extract_sentences, extract_words


@login_required
def get_detail(original):
    dictionary = get_collection('dictionary')
    word = dictionary.find_one({
        'user_id': ObjectId(current_user.id),
        'original': original
    })

    if word is None:
        return jsonify({'error': f'Word not found: {original}'}), 404

    articles_collection = get_collection('articles')

    articles = articles_collection.find(
        {'user_id': ObjectId(current_user.id), 'unique_words': {'$elemMatch': {'$eq': original}}},
        {'content': 1}
    )

    raw_sentences = [
        sentence
        for article in articles
        for paragraph in article['content'].split('\n')
        for sentence in extract_sentences(paragraph)
        if original in extract_words(sentence)
    ]

    sentences = [
        {'text': sentence, 'words': extract_words(sentence)}
        for sentence in list(set(raw_sentences))
    ]


    similar = dictionary.find({
        'user_id': ObjectId(current_user.id),
        'cluster_id': word['cluster_id']
    }, {'original': 1}) if word['cluster_id'] is not None else []


    return jsonify({
        'id': str(word['_id']),
        'original': word['original'],
        'translations': word['translations'],
        'frequency': word['frequency'],
        'status': word['status'],
        'sentences': sentences,
        'reviewLevel': word.get('review_level', 0),
        'lastViewed': word.get('last_viewed', None),
        'similar': [word['original'] for word in similar if word['original'] != original]
    })
