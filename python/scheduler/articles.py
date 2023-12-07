from utils.mongo_external import get_collection
from text_processing.extract import extract_words

def jobs():
    add_words()

def add_words():
    collection = get_collection('articles')

    query = {
        'content': {'$exists': True},
        'words': {'$exists': False}
    }

    if collection.count_documents(query) == 0:
        print('Nothing to do: All articles have a words array')
    else:
        articles = collection.find(query)
        for article in articles:
            words = extract_words(article['content'])
            article['words'] = words
            get_collection('articles').replace_one({'_id': article['_id']}, article)
            print('Added words to article: ' + article['title'] + f' ({len(words)})')
