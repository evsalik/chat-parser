from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.json'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with open(filepath, 'r') as f:
            data = json.load(f)
        statistics = {
            "total_messages": len(data),
            # Add more statistics here
        }
        return jsonify(statistics)
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)