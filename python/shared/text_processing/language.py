from utils.mongo import get_collection
from bson import ObjectId  # Import ObjectId for converting user_id

def get_languages(user_id):
    users_collection = get_collection('users')

    # Find the user in the users collection
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    if user:
        # Extract source and target languages from the user document
        source_language = user.get('sourceLanguage', 'en')
        target_language = user.get('targetLanguage', 'en')

        return source_language, target_language
    else:
        # Return default values if user is not found
        return 'en', 'en'
