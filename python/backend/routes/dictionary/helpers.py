from flask import jsonify

def select(word):
	return {
		'id': str(word['_id']),
		'original': word['original'],
		'translations': word['translations'],
		'status': word['status'],
		'frequency': word['frequency'],
	}

def serialize(word):
	return jsonify(select(word))

def serialize_many(words):
	return jsonify([select(word) for word in words])
