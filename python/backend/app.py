from flask import Flask
import logging
import sys

from migrations import migrate

from routes.articles import articles
from routes.dictionary import dictionary

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(logging.StreamHandler(sys.stdout))

# Register the Blueprint with the app
app.register_blueprint(articles, url_prefix='/api/articles')
app.register_blueprint(dictionary, url_prefix='/api/dictionary')

migrate()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
