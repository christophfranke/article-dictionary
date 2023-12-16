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
    return levenshtein_distance(word, other, score_cutoff=threshold) + penalty(word, other)

# find the smallest single distance in two arrays
def min_single_distance(words, others):
    return min([single_distance(word, other) for word in words for other in others])

# find the distance of two words
def distance(one, other):
    original_distance = single_distance(one['original'], other['original'])
    translation_distance = min_single_distance(one['translations'], other['translations'])
    # be a bit less permissive when it comes to translation distance
    return max(original_distance, translation_distance + 1)

def find_cluster(collection, word):
    closest_leader = None
    min_distance = float('inf')
    for other in collection.find({'user_id': word['user_id'], 'needs_retranslate': False}):
        if other['_id'] != word['_id']:
            dist = distance(other, word)
            if dist <= threshold and dist < min_distance:
                closest_leader = other['cluster_id']
                min_distance = dist
    return closest_leader

def update_leader(collection, new_word):
    leader_word = collection.find_one({'_id': new_word['cluster_id']})
    cluster_words = list(collection.find({'cluster_id': leader_word['_id']}))

    if (len(cluster_words) > 1):
        # Calculate the maximum distance of the current leader to any word in the cluster
        current_leader_max_dist = max(distance(leader_word, word) for word in cluster_words if word['_id'] != leader_word['_id'])

        # Calculate the maximum distance of the new word to any word in the cluster
        new_word_max_dist = max(distance(new_word, word) for word in cluster_words if word['_id'] != new_word['_id'])

        # Update the leader if the new word has a smaller maximum distance
        if new_word_max_dist < current_leader_max_dist:
            collection.update_many({'cluster_id': leader_word}, {'$set': {'cluster_id': new_word['_id']}})

def add_to_cluster(collection, word):
    closest_leader_id = find_cluster(collection, word)
    if closest_leader_id is None:
        collection.update_one({'_id': word['_id']}, {'$set': {'cluster_id': word['_id']}})
    else:
        collection.update_one({'_id': word['_id']}, {'$set': {'cluster_id': closest_leader_id}})
        update_leader(collection, word)
