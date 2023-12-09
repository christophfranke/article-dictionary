from flask import Flask
import logging
import sys
import secrets
from flask_login import LoginManager 

from routes.articles import articles
from routes.dictionary import dictionary
from routes.statistics import statistics
from routes.authentication import auth


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.config['SECRET_KEY'] = secrets.token_hex(16)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    # Assuming 'users' is the collection storing user data
    user_data = mongo_db.users.find_one({'_id': int(user_id)})
    if user_data:
        return User(user_data)

class User:
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.password_hash = user_data['password']



app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(articles, url_prefix='/api/articles')
app.register_blueprint(dictionary, url_prefix='/api/dictionary')
app.register_blueprint(statistics, url_prefix='/api/statistics')
