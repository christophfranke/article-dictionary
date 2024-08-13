from flask import Flask
import logging
import sys
import secrets
import os
from flask_login import LoginManager
from users import load_user
from mail import mail

from routes.articles import articles
from routes.dictionary import dictionary
from routes.statistics import statistics
from routes.authentication import auth
from routes.profile import profile
from routes.language import language
from routes.health_check import health_check


def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        # Load the test config if passed in
        app.config.update(config)
    else:
        # Routing
        app.config['EXTERNAL_HOSTNAME'] = os.environ.get('EXTERNAL_HOSTNAME', 'www.international-reader.com')
        app.config['EXTERNAL_PROTOCOL'] = os.environ.get('EXTERNAL_PROTOCOL', 'https')

        # Keys
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
        app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'main_app_salt')

        # Flask-Mail
        app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'None')
        app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1']
        app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() in ['true', '1']
        app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'None')
        app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'None')
        app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@international-reader.com')

        if os.environ.get('MAIL_SERVER') is None:
            print('Warning: MAIL_SERVER not set')
        if os.environ.get('MAIL_USERNAME') is None:
            print('Warning: MAIL_USERNAME not set')
        if os.environ.get('MAIL_PASSWORD') is None:
            print('Warning: MAIL_PASSWORD not set')

        # Cookies
        app.config['SESSION_COOKIE_SAMESITE'] = os.environ.get('SESSION_COOKIE_SAMESITE', 'Strict')
        app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ['true', '1']

        # Testing
        app.config['TESTING'] = os.environ.get('TESTING', 'False').lower() in ['true', '1']

    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))

    # Initialize Flask-Mail with the app
    mail.init_app(app)

    # Blueprints registration
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(profile, url_prefix='/api/profile')
    app.register_blueprint(articles, url_prefix='/api/articles')
    app.register_blueprint(dictionary, url_prefix='/api/dictionary')
    app.register_blueprint(statistics, url_prefix='/api/statistics')
    app.register_blueprint(language, url_prefix='/api/language')
    app.register_blueprint(health_check, url_prefix='/api')

    # Flask-Login setup
    login_manager = LoginManager(app)
    login_manager.user_loader(load_user)

    return app
