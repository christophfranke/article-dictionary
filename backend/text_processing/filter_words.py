from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import nltk

nltk.download('stopwords')

def filter_words(words, language="greek"):
    stop_words = set(stopwords.words(language))
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    filtered_words = [word for word in filtered_words if len(word) >= 2]

    return filtered_words

def extract_words(text, language="greek"):
    words = wordpunct_tokenize(text)
    return filter_words(words, language)