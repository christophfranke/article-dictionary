from utils.mongo_external import get_collection
from datetime import datetime
from bson import ObjectId


def repair():
    rename_languages()


def rename_languages():
    try:
        dictionary = get_collection('users')
        dictionary.update_many({}, {'$rename': {'sourceLanguage': 'source_language', 'targetLanguage': 'target_language'}})
    except Exception as e:
        print('Error renaming languages: ' + str(e))
