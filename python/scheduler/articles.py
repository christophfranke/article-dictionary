from utils.mongo_external import get_collection
from text_processing.extract import extract_words
from bson import ObjectId


def jobs():
    add_words()
    add_user_id()

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
