# html_generator.py
import os
import pandas as pd
from flask import render_template

# Function to read CSV file and generate HTML
def generate_html(file_path):
    df = pd.read_csv(file_path)
    title = os.path.splitext(os.path.basename(file_path))[0]
    return render_template('table.html', title=title, table=df.to_html(index=False))
