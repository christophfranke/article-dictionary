from utils.mongo_external import get_collection
from datetime import datetime
from bson import ObjectId


def jobs():
    create_statistics()


def create_user_statistics(user_id):
    dictionary = get_collection('dictionary')

    new_count = dictionary.count_documents({'status': 'new', 'user_id': user_id})
    seen_count = dictionary.count_documents({'status': 'seen', 'user_id': user_id})
    known_count = dictionary.count_documents({'status': 'known', 'user_id': user_id})
    ignore_count = dictionary.count_documents({'status': 'ignore', 'user_id': user_id})

    statistics = get_collection('statistics')

    statistics.insert_one({
        'user_id': user_id,
        'timestamp': datetime.utcnow(),
        'new_words': new_count,
        'seen_words': seen_count,
        'known_words': known_count,
        'ignore_words': ignore_count
    })

    print(f'Added statistics for user {user_id}')

def create_statistics():
    users_collection = get_collection('users')

    # Retrieve all users from the collection
    users = users_collection.find()

    for user in users:
        user_id = user['_id']
        create_user_statistics(user_id)

    print('Statistics creation for all users complete')
