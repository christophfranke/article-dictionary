from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk import download as nltk_download

nltk_download('stopwords')


def filter_words(words, language="greek"):
    stop_words = set(stopwords.words(language))
    filtered_words = [word for word in words if word.isalnum() and word.lower()]

    return filtered_words

def extract_words(text, language="greek"):
    words = wordpunct_tokenize(text)
    return filter_words(words, language)

def extract_unique_words(text, language="greek"):
    words = extract_words(text, language)
    return list(set([word.lower() for word in words]))