from text_processing.translate import translate_words
from text_processing.extract import extract_words

def add_text(text, dictionary_collection, language='greek'):
    words = extract_unique_words(text, language)
    add_words(words, dictionary_collection, language)

def add_words(words, dictionary_collection, language='greek'):
    new_words = []  # Array to collect yet-to-be-translated words

    for word in words:
        # Check if the word already exists in the dictionary
        existing_word = dictionary_collection.find_one({'original': word, 'language': language})

        if existing_word is None:
            # If the word is not in the dictionary, add it to the array
            new_words.append(word)
        else:
            print(f"Word '{word}' already exists in the dictionary.")

    # Assuming translate function returns an array of strings
    translations = translate_words(new_words, language)

    if (len(translations) != len(new_words)):
        print("Error: Number of translations does not match number of words.")

    # Iterate over the translations array and add each word to the dictionary
    for translated_word in translations:
        new_word = {
            'original': words[translations.index(translated_word)],
            'translated': translated_word,
            'status': 'new',
            'language': language
        }

        dictionary_collection.insert_one(new_word)
        print(f"Word '{new_word['original']}' added to the dictionary.")
