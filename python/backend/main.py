from flask import Flask
import logging
import sys
import secrets
from flask_login import LoginManager 
from users import load_user

from routes.articles import articles
from routes.dictionary import dictionary
from routes.statistics import statistics
from routes.authentication import auth
from routes.profile import profile
from routes.language import language


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(logging.StreamHandler(sys.stdout))

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_SECURE'] = False

app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(profile, url_prefix='/api/profile')
app.register_blueprint(articles, url_prefix='/api/articles')
app.register_blueprint(dictionary, url_prefix='/api/dictionary')
app.register_blueprint(statistics, url_prefix='/api/statistics')
app.register_blueprint(language, url_prefix='/api/language')

login_manager = LoginManager(app)
login_manager.user_loader(load_user)
