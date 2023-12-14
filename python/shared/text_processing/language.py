from bson import ObjectId  # Import ObjectId for converting user_id

def supported_languages():
    return {
        'en': 'English',
        'de': 'German',
        'fr': 'French',
        'es': 'Spanish',
        'pt': 'Portuguese',
        'el': 'Greek',
        'pl': 'Polish',
        'ru': 'Russian',
    }

def get_languages(users_collection, user_id):
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
