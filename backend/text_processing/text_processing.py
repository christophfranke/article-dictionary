import os
import pandas as pd
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from greek_stemmer_plus import GreekStemmer
from googletrans import Translator
from translation import translate_words
from sort_greek import sort_greek_alphabetically

def process_text(text, language='greek'):
    # Tokenize the text using wordpunct_tokenize for Greek text
    words = wordpunct_tokenize(text)
    # print('words:', words)

    # Remove common stopwords for the specified language
    stop_words = set(stopwords.words(language))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    filtered_words = [word for word in filtered_words if len(word) >= 2]
    # print('filtered_words:', filtered_words)

    # Use the Greek SnowballStemmer from snowballstemmer library
    stemmer = GreekStemmer()
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    # print('stemmed_words:', stemmed_words)

    unique_sorted_words = sort_greek_alphabetically(set(stemmed_words))

    return unique_sorted_words

def filter_common_words(words, common_words):
    # Remove common words from the list
    filtered_words = [word for word in words if word not in common_words]
    return filtered_words

def process_input(input_text):
    # Process the text
    processed_words = process_text(input_text, language='greek')

    # Define a list of common Greek words to filter out
    common_words_to_filter = ["κοινή_λέξη1", "κοινή_λέξη2", "κοινή_λέξη3"]  # Add your common words here

    # Filter out common words
    filtered_words = filter_common_words(processed_words, common_words_to_filter)

    # Translate and create a DataFrame
    translation_df = translate_words(filtered_words)

    return translation_df
