from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/export')
def export():
    subprocess.run(["/scripts/export.sh"])
    return "Export started."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
