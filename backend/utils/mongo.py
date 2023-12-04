from flask import g
from pymongo import MongoClient

username = 'root'
password = 'example'

def get_db():
    if 'db' not in g:
        # Create a MongoClient when it's not already available
        g.db = MongoClient(f'mongodb://{username}:{password}@mongodb:27017/')['dictionary_app_data']

    return g.db

def close_db(e=None):
    # Close the MongoClient connection if it exists
    db = g.pop('db', None)
    if db is not None:
        db.client.close()
