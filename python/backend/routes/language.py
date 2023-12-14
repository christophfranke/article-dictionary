from flask import Blueprint, jsonify
from text_processing.language import supported_languages

language = Blueprint('language', __name__)


@language.route('/supported')
def supported():
	return jsonify(supported_languages()), 200
