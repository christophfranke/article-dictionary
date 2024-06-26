from .jobs import retranslate_word, update_clusters, update_word_frequency
from .repair import remove_duplicates, remove_invalid_src_or_target, remove_no_original, add_cluster_id, add_review_level_and_last_reviewed, add_translation_origin


def jobs():
    retranslate_word()
    update_word_frequency()
    update_clusters()


def repair():
    print('Reparing dictionary...')
    # skip duplicates for now, calculations too costly
    # remove_duplicates()
    remove_invalid_src_or_target()
    remove_no_original()
    add_cluster_id()
    add_review_level_and_last_reviewed()
    add_translation_origin()
