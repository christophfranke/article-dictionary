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

        # Find word that meets the specified criteria
        query = {
            'original': {'$exists': True},  # Document must have the 'original' field
            '$or': [
                {'frequency': {'$exists': False}},  # 'frequency' is not set
                {'needs_recount': True},  # Needs Review is set to True
            ]
        }
        words = dictionary.find(query)

        articles = get_collection('articles').find()
        base_words = [word.lower() for sublist in [extract_words(a['content']) for a in articles] for word in sublist]
        word_frequencies = Counter(base_words)

        for word in words:
            frequency = word_frequencies[word['original']]

            # Update entry with frequency
            word['frequency'] = frequency
            word['needs_recount'] = False
            dictionary.replace_one({'_id': word['_id']}, word)

            print('Counted frequency for word: ' + word['original'] + ': ' + str(frequency))
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
                {'translations': {'$elemMatch': {'$regex': '\\.$'}}},  # Contains a dot in any translation
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

