from flask import jsonify

known_level = 4

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
	}

def serialize(word):
	return jsonify(select(word))

def serialize_many(words):
	return jsonify([select(word) for word in words])

def update_word(word, data):
	if 'translations' in data:
		word['needs_retranslate'] = False
		word['needs_clustering'] = True
		word['translation_origin'] = 'user'

	if not 'review_level' in word:
		word['review_level'] = known_level if word['status'] == 'known' else 0

	# status levels:
	# 0: new
	# 1: seen
	# 2: seen
	# 3: seen
	# 4: known
	# 5: known
	if 'status' in data:
		review_level = word.get('review_level', 0)
		if data['status'] == 'new':
			review_level = 0
		if data['status'] == 'seen' and review_level < 1:
			word['review_level'] = 1
		if data['status'] == 'seen' and review_level > known_level - 1:
			word['review_level'] = known_level - 1
		if data['status'] == 'known' and review_level < known_level:
			word['review_level'] = known_level

	allowed_keys = ['original', 'translations', 'status', 'frequency', 'last_viewed', 'review_level', 'needs_retranslate', 'needs_clustering', 'cluster_id']
	for json_key, value in data.items():
		key = camel_to_snake(json_key)
		if key in allowed_keys:
			word[key] = value

	return word
