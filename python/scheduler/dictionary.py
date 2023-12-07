from collections import Counter

from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word
from text_processing.extract import extract_words

def do_jobs():
    retranslate_word()
    remove_malformat()
    update_word_frequency()

def update_word_frequency():
    try:
        dictionary = get_collection('dictionary')

        # Find word that meets the specified criteria
        query = {
            'original': {'$exists': True},  # Document must have the 'original' field
            'status': {'$ne': 'ignore'},  # 'status' is not set to 'ignore'
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
            dictionary.replace_one({'_id': word['_id']}, word)

            print('Counted frequency for word: ' + word['original'] + ' - ' + str(frequency))
    except Exception as e:
        print('Error counting frequency for word: ' + str(e))

def retranslate_word():
    try:
        dictionary = get_collection('dictionary')

        # Find word that meets the specified criteria
        query = {
            'original': {'$exists': True},  # Document must have the 'original' field
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
            translations = translate_single_word(word['original'])

            # Update entry with translations
            word['translations'] = translations
            word['needs_retranslate'] = False
            dictionary.replace_one({'_id': word['_id']}, word)

            print('Translated word: ' + word['original'])
        else:
            print('No word to translate')
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
