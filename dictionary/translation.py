# translation.py

import pandas as pd
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from googletrans import Translator

def chunk_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def translate_words(words, chunk_size=500):
    translator = Translator()

    # Chunk the list of words into smaller lists
    word_chunks = chunk_list(words, chunk_size)

    # Translate each chunk of words
    translations = []
    for chunk in word_chunks:
        # Join the words in the chunk into a single string
        chunk_text = '.\n'.join(chunk)

        # Translate the chunk and split the translations back into a list
        chunk_translations = translator.translate(chunk_text, src='el', dest='en').text.split('.\n')

        # Append the translations to the overall list
        translations.extend(chunk_translations)

    # Repeat the translations if needed to match the length of words
    translations = translations[:len(words)]

    # print("Length of words:", len(words))
    # print("Length of translations:", len(translations))

    # print(words)
    # print(translations)

    # Create a DataFrame with the original and translated words
    df = pd.DataFrame({'Original': words, 'Translated': translations})

    return df
