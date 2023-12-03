from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from multiprocessing import Process

from html_generator import generate_html


app = Flask(__name__)

def external_function(name, text):
    # Simulate some asynchronous processing
    import time
    time.sleep(5)  # Simulate a delay

    # Save data or perform other processing here


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        text = request.form.get('text')

        # Start an asynchronous process to handle the external function
        process = Process(target=external_function, args=(name, text))
        process.start()

        # Redirect the user to '/' or '/[name]' after starting the process
        if name == '/':
            return redirect(url_for('index'))
        else:
            print(name)
            return redirect(url_for('serve_file', filename=name))

    return render_template('index.html')


# Route to handle requests for specific CSV files
@app.route('/<string:filename>')
def serve_file(filename):
    try:
        file_name = f"../data/{filename}.dict.csv"
        file_path = os.path.join(os.getcwd(), file_name)

        if os.path.isfile(file_path):
            return generate_html(file_path)
        else:
            return "File not found", 404
    except BrokenPipeError:
        return "Client disconnected", 200

if __name__ == '__main__':
    app.run(port=9300)
