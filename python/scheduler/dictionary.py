from collections import Counter

from utils.mongo_external import get_collection
from text_processing.translate import translate_single_word
from text_processing.extract import extract_words
from text_processing.dictionary import add_to_cluster, add_text
from bson import ObjectId


def jobs():
    retranslate_word()
    update_word_frequency()
    update_clusters()

def repair():
    remove_src_is_target()
    remove_duplicates()
    add_src_and_target_lang()
    remove_no_original()
    add_cluster_id()
    remove_zero_frequency()


def reset_word_frequency():
    dictionary = get_collection('dictionary')
    words = dictionary.find()

    for word in words:
        dictionary.update_one({'_id': word['_id']}, {
            '$set': {
                'needs_recount': True
            }
        })
    print('Reset word frequency')


def update_word_frequency():
    try:
        dictionary = get_collection('dictionary')
        article_collection = get_collection('articles')

        # Group by user_id and collect unique words from articles
        pipeline = [
            {
                '$match': {
                    'original': {'$exists': True},  # Document must have the 'original' field
                    '$or': [
                        {'frequency': {'$exists': False}},  # 'frequency' is not set
                        {'needs_recount': True},  # Needs Review is set to True
                    ]
                }
            },
            {
                '$lookup': {
                    'from': 'articles',
                    'localField': 'user_id',
                    'foreignField': 'user_id',
                    'as': 'articles'
                }
            },
            {
                '$unwind': '$articles'
            },
            {
                '$group': {
                    '_id': '$user_id',
                    'user_articles': {'$addToSet': '$articles.content'}
                }
            }
        ]

        user_articles = dictionary.aggregate(pipeline)

        for user_entry in user_articles:
            user_id = user_entry['_id']
            articles = user_entry['user_articles']
            user_word_frequencies = Counter()

            # Calculate word frequencies for the user
            for article_content in articles:
                base_words = extract_words(article_content)
                user_word_frequencies.update(base_words)

            # Update word frequencies for each word in the user's dictionary
            words_to_update = dictionary.find({'user_id': user_id, 'needs_recount': True})

            for word in words_to_update:
                frequency = user_word_frequencies[word['original']]

                # Update entry with frequency
                word['frequency'] = frequency
                word['needs_recount'] = False
                dictionary.replace_one({'_id': word['_id']}, word)

                if word['cluster_id'] is not None:
                    get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)
                print(f'Counted frequency for word {word["original"]}: {frequency}')

    except Exception as e:
        print('Error counting frequency for word: ' + str(e))


def retranslate_word():
    try:
        dictionary = get_collection('dictionary')

        # Find word that meets the specified criteria
        query = {
            'original': {'$exists': True},  # Document must have the 'original' field
            'source_language': {'$exists': True},  # Document must have the 'source_language' field
            'target_language': {'$exists': True},  # Document must have the 'target_language' field
            'status': {'$ne': 'ignore'},  # 'status' is not set to 'ignore'
            '$or': [
                {'translations': {'$elemMatch': {'$eq': ''}}},  # Empty translation entry in the array
                {'translations': {'$elemMatch': {'$regex': '#'}}},   # Contains a hash in any translation
                {'needs_retranslate': True},  # Needs Review is set to True
            ]
        }
        word = dictionary.find_one(query)

        if word:
            # Translate
            translations = translate_single_word(word['original'], word['source_language'], word['target_language'])

            # Update entry with translations
            word['translations'] = translations
            word['needs_retranslate'] = False
            word['needs_clustering'] = True
            if word['original'] in translations:
                word['status'] = 'ignore'
            dictionary.replace_one({'_id': word['_id']}, word)
            if word['cluster_id'] is not None:
                get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)

            print(f'Retranslated word {word["original"]}: {", ".join(map(str, translations))}')
    except Exception as e:
        print('Error retranslating word: ' + str(e))

def remove_zero_frequency():
    dictionary = get_collection('dictionary')

    # Find word that meets the specified criteria
    query = {
        'frequency': 0,  # Document must have the 'frequency' field
    }
    words = dictionary.find(query)

    for word in words:
        dictionary.delete_one({'_id': word['_id']})
        if word['cluster_id'] is not None:
            get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)
        print(f'Removed word: {word['original']} ({word['frequency']})')

def remove_no_original():
    dictionary = get_collection('dictionary')

    # Find word that meets the specified criteria
    query = {
        'original': {'$exists': False},  # Document must have the 'original' field
    }
    word = dictionary.find_one(query)

    if word:
        dictionary.delete_one({'_id': word['_id']})
        if word['cluster_id'] is not None:
            get_collection('cluster').update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)
        print('Removed word: ' + word)


def add_src_and_target_lang():
    collection = get_collection('dictionary')

    query = {
        'source_language': {'$exists': False},
        'target_language': {'$exists': False}
    }

    words = collection.find(query)

    for word in words:
        word['source_language'] = 'el'
        word['target_language'] = 'en'
        word.pop('language')
        collection.replace_one({'_id': word['_id']}, word)
        print('Added source and target language to word: ' + word['original'])


def remove_duplicates():
    collection = get_collection('dictionary')

    query = {
        'original': {'$exists': True},
        'source_language': {'$exists': True},
        'target_language': {'$exists': True},
        'user_id': {'$exists': True},
    }

    words = collection.find(query)

    for word in words:
        query = {
            'original': word['original'],
            'source_language': word['source_language'],
            'target_language': word['target_language'],
            'user_id': word['user_id'],
            '_id': {'$ne': word['_id']}
        }

        duplicate = collection.find_one(query)

        if duplicate:
            collection.delete_one({'_id': duplicate['_id']})
            print('Removed duplicate word: ' + duplicate['original'] + ' lang: ' + word['source_language'] + ' -> ' + word['target_language'])

def remove_src_is_target():
    collection = get_collection('dictionary')

    query = {
        'source_language': {'$exists': True},
        'target_language': {'$exists': True},
    }

    words = collection.find(query)

    for word in words:
        if word['source_language'] == word['target_language']:
            collection.delete_one({'_id': word['_id']})
            print('Removed malformat word: ' + word['original'] + ' lang: ' + word['source_language'] + ' -> ' + word['target_language'])

def add_cluster_id():
    dictionary = get_collection('dictionary')

    query = {
        '$and': [
            {
                '$or': [
                    {'needs_clustering': {'$exists': False}},
                    {'needs_clustering': True}
                ]
            },
            {
                '$or': [
                    {'cluster_id': {'$exists': False}},
                    {'cluster_id': None}
                ]
            }
        ]
    }

    words = dictionary.find(query)

    for word in words:
        word['cluster_id'] = word['_id']
        word['needs_clustering'] = True
        dictionary.replace_one({'_id': word['_id']}, word)
        print('Added cluster_id to word: ' + word['original'])

def reset_clusters():
    dictionary = get_collection('dictionary')
    cluster = get_collection('cluster')
    cluster.delete_many({})

    words = dictionary.find()

    for word in words:
        dictionary.update_one({'_id': word['_id']}, {
            '$set': {
                'needs_clustering': True,
                'cluster_id': word['_id']
            }
        })
    print('Reset clusters')

def update_clusters():
    dictionary = get_collection('dictionary')

    query = {
        'needs_clustering': True,
        'needs_retranslate': False,
    }

    words = dictionary.find(query).limit(25)

    for word in words:
        word['needs_clustering'] = False
        add_to_cluster(get_collection, word)
        dictionary.update_one({'_id': word['_id']}, {'$set': {'needs_clustering': False }})
        updated_word = dictionary.find_one({'_id': word['_id']})
        leader_word = dictionary.find_one({'_id': updated_word['cluster_id']})
        cluster_size = dictionary.count_documents({'cluster_id': leader_word['_id']})
        print(f'Updated cluster: {updated_word['original']} -> {leader_word['original']} ({cluster_size})')
