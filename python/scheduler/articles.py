from datetime import datetime
from bson import ObjectId

from text_processing.extract import extract_words, get_unique_words
from text_processing.characters import slugify
from utils.mongo_external import get_collection

from processing import process_article


def jobs():
    process_article()


def repair():
    add_needs_processing()
    add_reading_index()
    add_language()
    add_dates()
    add_status()
    add_privacy()
    add_owner()
    remove_dictionary()


def remove_words():
    collection = get_collection('articles')
    articles = collection.find()

    for article in articles:
        del article['words']
        del article['unique_words']
        collection.replace_one({'_id': article['_id']}, article)
        print('Removed words from article: ' + article['title'])


def add_needs_processing():
    collection = get_collection('articles')
    query = {
        'needs_processing': True,
    }

    count = collection.count_documents(query)

    # Update all documents that match the query
    if count == 0:
        result = collection.update_many({}, {'$set': {'needs_processing': True}})
        print(f"Added field 'needs_processing' to documents: {result.modified_count}/{result.matched_count}")
    else:
        print(f"Some documents ({count}) need processing, no reset.")


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


def add_reading_index():
    collection = get_collection('articles')

    query = {
        'reading_index': {'$exists': False}
    }

    articles = collection.find(query)

    for article in articles:
        article['reading_index'] = 0
        collection.replace_one({'_id': article['_id']}, article)
        print('Added word_index to article: ' + article['title'])
