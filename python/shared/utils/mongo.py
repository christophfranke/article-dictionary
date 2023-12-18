import os
from flask import g
from pymongo import MongoClient

username = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')
password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'example')
database = 'dictionary_app_data'

def get_db():
    if 'db' not in g:
        # Create a MongoClient when it's not already available
        g.db = MongoClient(f'mongodb://{username}:{password}@mongodb:27017/')[database]

    return g.db

def get_collection(collection_name):
    db = get_db()
    return db[collection_name]

def drop_collection(collection_name):
    db = get_db()
    db.drop_collection(collection_name)

def close_db(e=None):
    # Close the MongoClient connection if it exists
    db = g.pop('db', None)
    if db is not None:
        db.client.close()
