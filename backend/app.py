from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from collections import Counter, defaultdict
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def process_statistics(data):
    messages = data['messages']
    total_messages = len(messages)

    user_messages = Counter([message['from'] for message in messages if 'from' in message])
    most_active_user = user_messages.most_common(1)[0] if user_messages else ("N/A", 0)

    all_words = []
    for message in messages:
        if 'text' in message:
            if isinstance(message['text'], list):
                text_content = ' '.join([part['text'] for part in message['text'] if isinstance(part, dict) and 'text' in part])
            else:
                text_content = message['text']
            words = re.findall(r'\b\w+\b', text_content.lower())
            all_words.extend(words)
    word_frequencies = Counter(all_words).most_common(500)

    messages_per_day = Counter([datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").date().isoformat() for message in messages])
    messages_per_week = Counter(
        [f"{datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S').isocalendar()[0]}-W{datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S').isocalendar()[1]:02d}" for message in messages]
    )
    
    messages_per_weekday = Counter([datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").strftime('%A') for message in messages])

    first_message_per_day = defaultdict(list)
    for message in messages:
        date = datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").date().isoformat()
        first_message_per_day[date].append(message)

    first_message_count = Counter()
    for date, messages in first_message_per_day.items():
        first_message = min(messages, key=lambda x: x['date'])
        if 'from' in first_message:
            first_message_count[first_message['from']] += 1

    return {
        "total_messages": total_messages,
        "most_active_user": most_active_user,
        "user_message_counts": dict(user_messages),
        "user_percentages": {user: (count / total_messages) * 100 for user, count in user_messages.items()},
        "word_frequencies": word_frequencies,
        "messages_per_day": dict(messages_per_day),
        "messages_per_week": dict(messages_per_week),
        "messages_per_weekday": dict(messages_per_weekday),
        "first_message_count": dict(first_message_count)
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
