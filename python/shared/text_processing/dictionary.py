from text_processing.translate import translate_words
from text_processing.extract import extract_unique_words

def add_text(text, dictionary_collection, language='greek'):
    words = extract_unique_words(text, language)
    add_words(words, dictionary_collection)

def add_words(words, dictionary_collection):
    new_words = []  # Array to collect yet-to-be-translated words

    for word in words:
        # Check if the word already exists in the dictionary
        existing_word = dictionary_collection.find_one({'original': word})

        if existing_word is None:
            # If the word is not in the dictionary, add it to the array
            new_words.append(word)
        else:
            print(f"Word '{word}' already exists in the dictionary.")

    # Assuming translate function returns a dictionary
    try:
        translations = translate_words(new_words)
    except Exception as e:
        raise Exception(f'Error translating words: {e}')

    if not set(new_words).issubset(translations.keys()):
        raise Exception(f'Translations do not cover all new words: {translations}')

    # Iterate over the translations dictionary and add each word to the dictionary
    for original_word, translation_possibilities in translations.items():
        trans = translation_possibilities
        primary = trans[0] if len(trans) > 0 else original_word
        status = 'new' if (len(trans) > 0 and original_word != primary) or len(trans) == 0 else 'ignore'
        new_word = {
            'original': original_word,
            'translations': [primary],
            'status': status,
            'language': 'greek',
            'needs_review': True,
        }

        dictionary_collection.insert_one(new_word)
        print(f"Word '{new_word['original']}' added to the dictionary.")
