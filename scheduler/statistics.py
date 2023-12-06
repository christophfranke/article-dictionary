from mongo import get_collection
from datetime import datetime

def create_statistics():
    dictionary = get_collection('dictionary')

    new_count = dictionary.count_documents({'status': 'new'})
    seen_count = dictionary.count_documents({'status': 'seen'})
    known_count = dictionary.count_documents({'status': 'known'})
    ignore_count = dictionary.count_documents({'status': 'ignore'})

    statistics = get_collection('statistics')

    statistics.insert_one({
        'timestamp': datetime.utcnow(),
        'new_words': new_count,
        'seen_words': seen_count,
        'known_words': known_count,
        'ignore_words': ignore_count
    })

    print('Added statistics')