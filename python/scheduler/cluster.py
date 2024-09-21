from utils.mongo_external import get_collection
from bson import ObjectId


CLUSTER_ATTRIBUTE_UPDATE_LIMIT = 50


def jobs():
    update_aggregate_attributes()
    # recalculate_all()


def repair():
    create_clusters()


def create_clusters():
    dictionary = get_collection('dictionary')
    cluster = get_collection('cluster')

    words = dictionary.find({
        'lemma': {'$exists': True},
        'cluster_id': {'$exists': True},
        'needs_clustering': False,
    })

    recluster_word = 0
    clusters_reset = 0

    for word in words:
        original = word.get('original')
        cluster_id = word.get('cluster_id')
        if cluster_id is None:
            print(f'Skiped because Word has no cluster_id: {original}')
            continue
        cluster_entry = cluster.find_one({'_id': cluster_id})
        if cluster_entry is None:
            dictionary.update_one({'_id': word['_id']}, {'$set': {'needs_clustering': True}})
            print(f'Marked word for recluster {original} -> {word['lemma']} (current cluster does not exist)')
            recluster_word += 1
            continue

        status = cluster_entry.get('status', None)
        needs_recalculation = cluster_entry.get('needs_recalculation')
        if status is None and needs_recalculation is not True:
            cluster.update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}})
            print(f'Reset cluster for word {original} (Had no status)')
            clusters_reset += 1

    # print(f'\n\nMarked {recluster_word} words for recluster.\nReset {clusters_reset} clusters.\n\n')


def recalculate_all():
    collection = get_collection('cluster')

    count = collection.count_documents({
        'needs_recalculation': True
    })

    if count == 0:
        result = collection.update_many({}, {'$set': {'needs_recalculation': True}})
        print(f"Added field 'needs_recalculation' to clusters: {result.modified_count}/{result.matched_count}")


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

    # cluster_data_entries = cluster.count_documents(query)
    # print(f'\n\n\nUpdating cluster data for {CLUSTER_ATTRIBUTE_UPDATE_LIMIT}/{cluster_data_entries} clusters.\n')

    for entry in cluster.find(query).limit(CLUSTER_ATTRIBUTE_UPDATE_LIMIT):
        lead_word = dictionary.find_one({'_id': entry['_id']})
        if not lead_word:
            cluster.delete_one({'_id': entry['_id']})
            print(f'Deleted cluster, because it has no lead word: {entry.get("_id", "No Id")} ({str(entry.get("originals", []))}.')
            continue

        if lead_word['needs_clustering']:
            print(f'Skip cluster data, needs clustering first: {lead_word["original"]}')
            continue

        if ObjectId(lead_word['cluster_id']) != ObjectId(lead_word['_id']):
            new_cluster_leader = dictionary.find_one({'_id': lead_word['cluster_id']})
            cluster.delete_one({'_id': entry['_id']})
            dictionary.update_one({'_id': lead_word['_id']}, {'$set': {'needs_clustering': True}})

            if new_cluster_leader is not None:
                dictionary.update_one({'_id': new_cluster_leader['_id']}, {'$set': {'needs_clustering': True}})
                print(f'Lead word: {str(lead_word['original'])} has new cluster leader {str(new_cluster_leader['original'])}, cluster dropped: {entry["_id"]} ({lead_word["original"]})')
            else:
                print(f'Lead word: {str(lead_word['original'])} has no cluster leader, cluster dropped: {entry["_id"]} ({lead_word["original"]})')
            continue

        cluster_words = list(dictionary.find({'cluster_id': entry['_id']}))
        if not cluster_words:
            print(f'Skip word: Could not find cluster words for cluster: {entry["_id"]} ({lead_word["original"]})')
            continue

        try:
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
            print(f'Updated cluster {lead_word.get('original')} (size: {len(originals)}, {entry.get('status')}) -> {str(translations[:3])} (freq: {frequency}, status: {status})')

        except TypeError as e:
            print(f"TypeError encountered: {e}")
            # dictionary.update_many({'cluster_id': entry['_id']}, {'$set': {
            #     'needs_retranslate': True
            # }})
            # get_collection('translations').delete_many({'original': {
            #     '$in': [word['original'] for word in cluster_words]
            # }})
            print(f"Data causing error: {cluster_words}")
            # print(f"Try to fix with retranslate...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(f"Data causing error: {cluster_words}")
