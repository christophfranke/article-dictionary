from flask import Flask
from routes.hello import hello_bp  # Import the Blueprint from routes/hello.py

app = Flask(__name__)

# Register the Blueprint with the app
app.register_blueprint(hello_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
