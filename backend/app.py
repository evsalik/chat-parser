from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from collections import Counter

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
app.config['UPLOAD_FOLDER'] = 'uploads/'

def process_statistics(data):
    messages = data['messages']
    total_messages = len(messages)

    # Count messages by each user
    user_messages = Counter([message['from'] for message in messages if 'from' in message])
    most_active_user = user_messages.most_common(1)[0] if user_messages else ("N/A", 0)

    # Calculate percentage of messages by each user
    user_percentages = {user: (count / total_messages) * 100 for user, count in user_messages.items()}
    
    return {
        "total_messages": total_messages,
        "most_active_user": most_active_user,
        "user_percentages": user_percentages,
        "user_message_counts": user_messages
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
