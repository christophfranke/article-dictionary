from utils.mongo_external import get_collection


def jobs():
    update_aggregate_attributes()


def max_status(statuses):
    # Convert generator to a set to handle multiple occurrences efficiently
    status_set = set(statuses)

    if 'known' in status_set:
        return 'known'
    if 'seen' in status_set:
        return 'seen'
    if 'new' in status_set:
        return 'new'
    if 'ignore' in status_set:
        return 'ignore'

    # Optionally return a default value or None if no status matches
    return None


def update_aggregate_attributes():
    dictionary = get_collection('dictionary')
    cluster = get_collection('cluster')

    query = {
        'needs_recalculation': True
    }

    for entry in cluster.find(query).limit(25):
        lead_word = dictionary.find_one({'_id': entry['_id']})
        if not lead_word:
            cluster.delete_one({'_id': entry['_id']})
            print(f'Deleted cluster, because it has no lead word: {entry.get("_id", "No Id")}: {entry.get("original", "No original word")}.')
            continue

        if lead_word['cluster_id'] != lead_word['_id']:
            print(f'Lead word has changed, cluster dropped: {entry["_id"]} ({lead_word["original"]})')
            cluster.delete_one({'_id': entry['_id']})
            continue

        cluster_words = list(dictionary.find({'cluster_id': entry['_id']}))
        if not cluster_words:
            print(f'Error: Could not find cluster words for cluster: {entry["_id"]} ({lead_word["original"]})')
            continue

        status = max_status(one['status'] for one in cluster_words)
        frequency = sum(word['frequency'] for word in cluster_words)
        originals = [word['original'] for word in cluster_words]
        translations = list(set([
            translation
            for word in cluster_words
            for translation in word['translations']
        ]))

        data = {
            'user_id': lead_word['user_id'],
            'source_language': lead_word['source_language'],
            'target_language': lead_word['target_language'],
            'originals': originals,
            'translations': translations,
            'status': status,
            'frequency': frequency,
            'needs_recalculation': False
        }

        cluster.update_one({'_id': entry['_id']}, {'$set': data})
        print(f'Updated cluster data: {str(originals)} -> {str(translations)} (freq: {frequency}, status: {status})')
