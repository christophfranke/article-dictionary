from collections import Counter
from pymongo import InsertOne, UpdateOne
from bson import ObjectId

from utils.mongo_external import get_collection
from nlp.analyze import process
from text_processing.dictionary import add_words
from text_processing.language import get_languages

from nlp.add_tokens import add_tokens


def process_article():
    collection = get_collection('articles')
    article = collection.find_one({
        'needs_processing': True
    })

    if article is not None:
        user_id = ObjectId(article.get('user_id'))
        if user_id is None:
            print(f"Article has no user_id: {article.title}")
            return
        user = get_collection('users').find_one({'_id': user_id})
        if user is None:
            print(f"Article has invalid user_id: {article.title}, {user_id}")
            return

        src_lang, target_lang = user.get('source_language'), user.get('target_language')
        tokens = process(article['content'], src_lang, target_lang)

        add_tokens(tokens, user_id)

        collection.update_one({'_id': ObjectId(article.get('_id'))}, {
            '$set': {
                'tokens': tokens,
                'needs_processing': False,
            }
        })

        print(f"Processed article: {article['title']} ({src_lang} -> {target_lang})")
