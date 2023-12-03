import pandas as pd
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from googletrans import Translator
import os

def chunk_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def load_dictionary(dictionary_file):
    if os.path.exists(dictionary_file):
        df = pd.read_csv(dictionary_file)
        return dict(zip(df['Original'], df['Translated']))
    else:
        return {}

def save_to_dictionary(word, translation, dictionary_file='dictionary.csv'):
    data = {'Original': [word], 'Translated': [translation]}
    df = pd.DataFrame(data)
    
    if os.path.exists(dictionary_file):
        existing_df = pd.read_csv(dictionary_file)
        df = pd.concat([existing_df, df], ignore_index=True)

    # Sort the DataFrame by the 'Original' column
    df = df.sort_values(by='Original', ignore_index=True)

    df.to_csv(dictionary_file, index=False)


def translate_words(words, dictionary_file='dictionary.csv', chunk_size=500):
    translator = Translator()

    # Load translations from the dictionary file
    dictionary = load_dictionary(dictionary_file)

    # Check which words have translations in the dictionary
    translated_words = [dictionary.get(word, None) for word in words]

    # Filter out words with translations from the list
    words_to_translate = [word for word, translation in zip(words, translated_words) if translation is None]

    print('Translated words:', len(translated_words))
    print('Words to translate:', len(words_to_translate))

    translations = []
    if len(words_to_translate) > 0:
        # Chunk the list of words to be translated into smaller lists
        word_chunks = chunk_list(words_to_translate, chunk_size)

        # Translate each chunk of words
        for chunk in word_chunks:
            # Join the words in the chunk into a single string
            chunk_text = '.\n'.join(chunk)

            # Translate the chunk and split the translations back into a list
            chunk_translations = translator.translate(chunk_text, src='el', dest='en').text.split('.\n')

            # Append the translations to the overall list
            translations.extend(chunk_translations)

    # Combine translations from the dictionary and the translator
    final_translations = translated_words.copy()
    for i, translation in enumerate(translations):
        if translated_words[i] is None:
            final_translations[i] = translation

    # Create a DataFrame with the original and final translated words
    df = pd.DataFrame({'Original': words, 'Translated': final_translations})

    # Save new translations to the dictionary
    for word, translation in zip(words_to_translate, translations):
        save_to_dictionary(word, translation, dictionary_file)

    return df

# Example usage:
# translate_words(["word1", "word2", "word3"])
