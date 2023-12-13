from nltk.tokenize import wordpunct_tokenize, sent_tokenize

from nltk import download
download('punkt')

def filter_words(words):
    filtered_words = [word for word in words if word.isalnum() and word.lower()]
    return filtered_words

def extract_words(text):
    words = wordpunct_tokenize(text)
    return filter_words(words)

def extract_unique_words(text):
    words = extract_words(text)
    return list(set([word.lower() for word in words]))

def extract_sentences(text):
    return sent_tokenize(text)