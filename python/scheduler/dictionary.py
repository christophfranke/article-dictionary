from collections import Counter

from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word
from text_processing.extract import extract_words
from bson import ObjectId


def jobs():
    retranslate_word()
    remove_malformat()
    update_word_frequency()
    add_user_id()
    add_src_and_target_lang()

def update_word_frequency():
    try:
        dictionary = get_collection('dictionary')
        article_collection = get_collection('articles')

        # Group by user_id and collect unique words from articles
        pipeline = [
            {
                '$match': {
                    'original': {'$exists': True},  # Document must have the 'original' field
                    '$or': [
                        {'frequency': {'$exists': False}},  # 'frequency' is not set
                        {'needs_recount': True},  # Needs Review is set to True
                    ]
                }
            },
            {
                '$lookup': {
                    'from': 'articles',
                    'localField': 'user_id',
                    'foreignField': 'user_id',
                    'as': 'articles'
                }
            },
            {
                '$unwind': '$articles'
            },
            {
                '$group': {
                    '_id': '$user_id',
                    'user_articles': {'$addToSet': '$articles.content'}
                }
            }
        ]

        user_articles = dictionary.aggregate(pipeline)

        for user_entry in user_articles:
            user_id = user_entry['_id']
            articles = user_entry['user_articles']
            user_word_frequencies = Counter()

            # Calculate word frequencies for the user
            for article_content in articles:
                base_words = extract_words(article_content)
                user_word_frequencies.update([base_word.lower() for base_word in base_words])

            # Update word frequencies for each word in the user's dictionary
            words_to_update = dictionary.find({'user_id': user_id, 'needs_recount': True})

            for word in words_to_update:
                frequency = user_word_frequencies[word['original']]

                # Update entry with frequency
                word['frequency'] = frequency
                word['needs_recount'] = False
                dictionary.replace_one({'_id': word['_id']}, word)

                print(f'Counted frequency for word {word["original"]} for user {user_id}: {frequency}')

    except Exception as e:
        print('Error counting frequency for word: ' + str(e))


def retranslate_word():
    try:
        dictionary = get_collection('dictionary')

        # Find word that meets the specified criteria
        query = {
            'original': {'$exists': True},  # Document must have the 'original' field
            'source_language': {'$exists': True},  # Document must have the 'source_language' field
            'target_language': {'$exists': True},  # Document must have the 'target_language' field
            'status': {'$ne': 'ignore'},  # 'status' is not set to 'ignore'
            '$or': [
                {'translations': {'$elemMatch': {'$eq': ''}}},  # Empty translation entry in the array
                {'translations': {'$elemMatch': {'$regex': '#'}}},   # Contains a hash in any translation
                {'needs_retranslate': True},  # Needs Review is set to True
            ]
        }
        word = dictionary.find_one(query)

        if word:
            # Translate
            translations = translate_single_word(word['original'], word['source_language'], word['target_language'])

            # Update entry with translations
            word['translations'] = translations
            word['needs_retranslate'] = False
            dictionary.replace_one({'_id': word['_id']}, word)

            print(f'Retranslated word {word["original"]}: {", ".join(map(str, translations))}')
    except Exception as e:
        print('Error retranslating word: ' + str(e))


def remove_malformat():
    dictionary = get_collection('dictionary')

    # Find word that meets the specified criteria
    query = {
        'original': {'$exists': False},  # Document must have the 'original' field
    }
    word = dictionary.find_one(query)

    if word:
        dictionary.delete_one({'_id': word['_id']})
        print('Removed word: ' + word)


krito_id = ObjectId('657488efbf4ba7afa277e164')
def add_user_id():
    collection = get_collection('dictionary')

    query = {
        'user_id': {'$exists': False}
    }

    words = collection.find(query)

    for word in words:
        word['user_id'] = krito_id
        collection.replace_one({'_id': word['_id']}, word)
        print('Added user_id to word: ' + word['original'])


def add_src_and_target_lang():
    collection = get_collection('dictionary')

    query = {
        'source_language': {'$exists': False},
        'target_language': {'$exists': False}
    }

    words = collection.find(query)

    for word in words:
        word['source_language'] = 'el'
        word['target_language'] = 'en'
        word.pop('language')
        collection.replace_one({'_id': word['_id']}, word)
        print('Added source and target language to word: ' + word['original'])

