from datetime import datetime
from bson import ObjectId

from text_processing.extract import extract_words
from utils.mongo_external import get_collection


def jobs():
    add_words()
    add_user_id()
    add_language()
    add_dates()
    add_status()

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

krito_id = ObjectId('657488efbf4ba7afa277e164')
def add_user_id():
    collection = get_collection('articles')

    query = {
        'user_id': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['user_id'] = krito_id
        collection.replace_one({'_id': article['_id']}, article)
        print('Added user_id to article: ' + article['title'])

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
