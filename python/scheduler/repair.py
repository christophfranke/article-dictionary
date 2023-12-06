from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word

def repair_word():
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
            ]
        }
        word = dictionary.find_one(query)

        if word:
            # Translate
            translations = translate_single_word(word['original'])

            # Update entry with translations
            word['translations'] = translations
            dictionary.replace_one({'_id': word['_id']}, word)

            print('Repaired word: ' + word['original'])
        else:
            print('No word to repair')
    except Exception as e:
        print('Error repairing word: ' + str(e))