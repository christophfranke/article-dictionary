from datetime import datetime
from bson import ObjectId

from text_processing.extract import extract_words, get_unique_words
from utils.mongo_external import get_collection


def jobs():
    pass

def repair():
    add_words()
    add_language()
    add_dates()
    add_status()
    add_privacy()
    add_owner()
    remove_dictionary()
    add_unique_words()

def add_words():
    collection = get_collection('articles')

    query = {
        'content': {'$exists': True},
        'words': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        words = extract_words(article['content'])
        article['words'] = words
        get_collection('articles').replace_one({'_id': article['_id']}, article)
        print('Added words to article: ' + article['title'] + f' ({len(words)})')

def add_language():
    collection = get_collection('articles')

    query = {
        'language': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['language'] = 'el'
        collection.replace_one({'_id': article['_id']}, article)
        print('Added language to article: ' + article['title'])

def add_dates():
    collection = get_collection('articles')

    query = {
        'created_at': {'$exists': False},
        'last_read': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['created_at'] = datetime.utcnow()
        article['last_read'] = datetime.utcnow()
        collection.replace_one({'_id': article['_id']}, article)
        print('Added dates to article: ' + article['title'])

def add_status():
    collection = get_collection('articles')

    query = {
        'status': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['status'] = 'new'
        collection.replace_one({'_id': article['_id']}, article)
        print('Added status to article: ' + article['title'])

def add_privacy():
    collection = get_collection('articles')

    query = {
        'privacy': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['privacy'] = 'public'
        collection.replace_one({'_id': article['_id']}, article)
        print('Added privacy to article: ' + article['title'])

def add_owner():
    collection = get_collection('articles')

    query = {
        'owner_id': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['owner_id'] = article['user_id']
        collection.replace_one({'_id': article['_id']}, article)
        print('Added owner_id to article: ' + article['title'])

def remove_dictionary():
    collection = get_collection('articles')

    query = {
        'dictionary': {'$exists': True}
    }

    articles = collection.find(query)

    for article in articles:
        del article['dictionary']
        collection.replace_one({'_id': article['_id']}, article)
        print('Removed dictionary from article: ' + article['title'])

def add_unique_words():
    collection = get_collection('articles')

    query = {
        'unique_words': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['unique_words'] = get_unique_words(article['words'])
        collection.replace_one({'_id': article['_id']}, article)
        print('Added unique_words to article: ' + article['title'])