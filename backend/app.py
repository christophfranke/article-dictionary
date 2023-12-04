from flask import Flask
from routes.hello import hello_bp  # Import the Blueprint from routes/hello.py
from routes.articles import articles  # Import the Blueprint from routes/hello.py

app = Flask(__name__)

# Register the Blueprint with the app
app.register_blueprint(hello_bp)
app.register_blueprint(articles, url_prefix='/api/articles')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
