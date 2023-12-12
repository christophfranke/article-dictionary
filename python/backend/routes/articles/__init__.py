from flask import Blueprint

from .list import list_articles
from .create import create_article
from .get import get_article
from .update import update_article
from .read import read_article


articles = Blueprint('articles', __name__)

articles.route('/')(list_articles)
articles.route('/create', methods=['POST'])(create_article)
articles.route('/<slug>', methods=['GET'])(get_article)
articles.route('/<slug>', methods=['PUT'])(update_article)
articles.route('/seen', methods=['POST'])(read_article)
