from utils.mongo import get_collection
from bson import ObjectId

def load_user(user_id):
    print('loading user', user_id)
    user_data = get_collection('users').find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)

class User:
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.password_hash = user_data['password']
        self.is_active = True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True
