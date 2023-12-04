from flask import Blueprint

articles = Blueprint('articles', __name__)

@articles.route('/')
def list():
    return '[]'
