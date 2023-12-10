from utils.mongo import get_collection
from bson import ObjectId  # Import ObjectId for converting user_id

def get_languages(user_id):
    users_collection = get_collection('users')

    # Find the user in the users collection
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    if user:
        # Extract source and target languages from the user document
        source_language = user.get('source_language', 'en')
        target_language = user.get('target_language', 'de')

        return source_language, target_language
    else:
        # Log a warning or handle the case where user is not found
        print(f"User not found for user_id: {user_id}")

        # Return default values if user is not found
        return 'en', 'de'
