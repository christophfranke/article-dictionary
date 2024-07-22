from utils.mongo_external import get_collection
from bson import ObjectId
from nlp.analyze import process


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

        print(f"Found article to process: {article['title']}")
        print(article.keys())
        print(f"{src_lang} -> {target_lang}")

        process(article['content'], src_lang, target_lang)
