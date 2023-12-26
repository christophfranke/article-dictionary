from flask import Blueprint

from .list import list_words
from .reset import reset_dictionary
from .update_one import update_word
from .update_many import update_many
from .retranslate import retranslate
from .add import add_word
from .seen import seen_word
from .detail import get_detail

dictionary = Blueprint('dictionary', __name__)

dictionary.route('/')(list_words)
dictionary.route('/reset', methods=['POST'])(reset_dictionary)
dictionary.route('/update/<id>', methods=['PUT'])(update_word)
dictionary.route('/update/', methods=['PUT'])(update_many)
dictionary.route('/retranslate/<id>', methods=['POST'])(retranslate)
dictionary.route('/add', methods=['POST'])(add_word)
dictionary.route('/seen/<id>', methods=['POST'])(seen_word)
dictionary.route('/<original>')(get_detail)
