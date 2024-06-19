from Levenshtein import distance as levenshtein_distance

# distances bigger than that will not be considered
threshold = 3


# made for a threshold of 3
# words of length 1 allow 0 edits
# words of length 2-3 allow 1 edit
# words of length 4-5 allow 2 edits
# words of length > 5 allow 3 edits
def penalty(word, other):
    length = 0.5 * (len(word) + len(other))
    return max(0, 3 - 0.5 * length)


def single_distance(word, other):
    return levenshtein_distance(word.lower(), other.lower(), score_cutoff=threshold) + penalty(word, other)


# find the smallest single distance in two arrays
def min_single_distance(words, others):
    return min([single_distance(word, other) for word in words for other in others])


# find the distance of two words
def distance(one, other):
    original_distance = single_distance(one['original'], other['original'])
    translation_distance = min_single_distance(one['translations'], other['translations'])
    # be a bit less permissive when it comes to translation distance
    return max(original_distance, translation_distance + 1.5)


def find_cluster(get_collection, word):
    closest_leader = None
    min_distance = float('inf')
    for other in get_collection('dictionary').find({'user_id': word['user_id'], 'needs_retranslate': False}):
        if other['_id'] != word['_id']:
            dist = distance(other, word)
            if dist <= threshold and dist < min_distance:
                closest_leader = other['cluster_id']
                min_distance = dist
    return closest_leader


def update_leader(get_collection, new_word):
    dictionary = get_collection('dictionary')
    leader_word = dictionary.find_one({'_id': new_word['cluster_id']})
    cluster_words = list(dictionary.find({'cluster_id': leader_word['_id']}))

    if (len(cluster_words) > 1):
        # Calculate the maximum distance of the current leader to any word in the cluster
        current_leader_max_dist = max(distance(leader_word, word) for word in cluster_words if word['_id'] != leader_word['_id'])

        # Calculate the maximum distance of the new word to any word in the cluster
        new_word_max_dist = max(distance(new_word, word) for word in cluster_words if word['_id'] != new_word['_id'])

        # Update the leader if the new word has a smaller maximum distance
        if new_word_max_dist < current_leader_max_dist:
            dictionary.update_many({'cluster_id': leader_word}, {'$set': {'cluster_id': new_word['_id']}})


def remove_from_cluster(get_collection, word):
    # Check if the word being removed is the current leader
    dictionary = get_collection('dictionary')
    if word['_id'] == word['cluster_id']:
        cluster_words = list(dictionary.find({'cluster_id': word['_id']}))

        # If there are other words in the cluster
        if len(cluster_words) > 1:
            # Remove the current leader from the list
            cluster_words = [w for w in cluster_words if w['_id'] != word['_id']]

            if len(cluster_words) == 1:
                # If there is only one word left in the cluster, make it the leader
                last_word = cluster_words[0]
                dictionary.update_one({'_id': last_word['_id']}, {'$set': {'cluster_id': last_word['_id']}})

            else:
                # Find the new leader based on the specified criteria (e.g., minimum average distance)
                min_max_dist = float('inf')
                new_leader = None
                for candidate in cluster_words:
                    max_distance = max(
                        distance(candidate, other) for other in cluster_words if other['_id'] != candidate['_id']
                    )
                    if max_distance < min_max_dist:
                        min_max_dist = max_distance
                        new_leader = candidate

                # Update the cluster_id for the cluster
                if new_leader:
                    dictionary.update_many({'cluster_id': word['_id']}, {'$set': {'cluster_id': new_leader['_id']}})
                else:
                    # If no new leader was found, dissolve the cluster
                    for cluster_word in cluster_words:
                        dictionary.update_one({'_id': cluster_word['_id']}, {'$set': {
                            'cluster_id': cluster_word['_id'],
                            'needs_clustering': True
                        }})


def add_to_cluster(get_collection, word):
    cluster = get_collection('cluster')
    if word['cluster_id'] is not None:
        cluster.update_one({'_id': word['cluster_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)
        remove_from_cluster(get_collection, word)

    closest_leader_id = find_cluster(get_collection, word)

    dictionary = get_collection('dictionary')
    if closest_leader_id is None:
        if word['_id'] is None:
            raise Exception(f'Cannot add to cluster: Word has no _id {word['original']}')
        dictionary.update_one({'_id': word['_id']}, {'$set': {'cluster_id': word['_id']}})
        cluster.update_one({'_id': word['_id']}, {'$set': {'needs_recalculation': True}}, upsert=True)
    else:
        dictionary.update_one({'_id': word['_id']}, {'$set': {'cluster_id': closest_leader_id}})
        word['cluster_id'] = closest_leader_id
        update_leader(get_collection, word)
        cluster.update_one({'_id': closest_leader_id}, {'$set': {'needs_recalculation': True}}, upsert=True)
