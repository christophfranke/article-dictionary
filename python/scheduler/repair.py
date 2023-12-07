from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word

def repair():
    repair_word()
    remove_malformat()

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
                {'needs_review': True}  # Needs Review is set to True
#                {'needs_review': {'$exists': False}}  # 'needs_review' does not exist
            ]
        }
        word = dictionary.find_one(query)

        if word:
            # Translate
            translations = translate_single_word(word['original'])

            # Update entry with translations
            word['translations'] = translations
            word['needs_review'] = False
            dictionary.replace_one({'_id': word['_id']}, word)

            print('Repaired word: ' + word['original'])
        else:
            print('No word to repair')
    except Exception as e:
        print('Error repairing word: ' + str(e))

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
