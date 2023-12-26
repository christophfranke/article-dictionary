from flask import jsonify

def select(word):
	return {
		'id': str(word['_id']),
		'cluster_id': str(word.get('cluster_id', word['_id'])),
		'original': word.get('original', ''),
		'translations': word.get('translations', []),
		'status': word.get('status', 'new'),
		'frequency': word.get('frequency', 0),
		'lastViewed': word.get('last_viewed', ''),
		'reviewLevel': word.get('review_level', 3 if word['status'] == 'known' else 0),
	}

def serialize(word):
	return jsonify(select(word))

def serialize_many(words):
	return jsonify([select(word) for word in words])
