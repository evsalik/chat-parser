from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from collections import Counter
import re

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def process_statistics(data):
    messages = data['messages']
    total_messages = len(messages)

    user_messages = Counter([message['from'] for message in messages if 'from' in message])
    most_active_user = user_messages.most_common(1)[0] if user_messages else ("N/A", 0)
    
    text_content = ' '.join(
        [message['text'] if isinstance(message['text'], str) else ' '.join([part['text'] for part in message['text'] if isinstance(part, dict)]) for message in messages if 'text' in message]
    ).lower()
    words = re.findall(r'\b\w+\b', text_content)
    word_frequencies = Counter(words).most_common(500)

    return {
        "total_messages": total_messages,
        "most_active_user": most_active_user,
        "user_message_counts": dict(user_messages),
        "user_percentages": {user: (count / total_messages) * 100 for user, count in user_messages.items()},
        "word_frequencies": word_frequencies
    }

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
        with open(filepath) as f:
            data = json.load(f)
            statistics = process_statistics(data)
        return jsonify(statistics)
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
