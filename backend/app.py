from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
import logging

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

logging.basicConfig(level=logging.DEBUG)

def process_statistics(data):
    messages = data.get('messages', [])
    total_messages = len(messages)

    user_messages = Counter([message.get('from', 'Unknown') if message.get('from') is not None else 'Unknown' for message in messages if 'from' in message])
    most_active_user = user_messages.most_common(1)[0] if user_messages else ("N/A", 0)

    all_words = []
    laugh_count = 0
    for message in messages:
        if 'text' in message:
            if isinstance(message['text'], list):
                text_content = ' '.join([part.get('text', '') for part in message['text'] if isinstance(part, dict) and 'text' in part])
            else:
                text_content = message['text']
            words = re.findall(r'\b\w+\b', text_content.lower())
            all_words.extend(words)

            if re.search(r'\b(ахах|хах|хаха|пазх|пах|ахзп|азпахз|апх|апз|аппа)\w*\b', text_content, re.IGNORECASE):
                laugh_count += 1
    word_frequencies = Counter(all_words).most_common(500)

    messages_per_day = Counter(
        [datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").date().isoformat() for message in messages if 'date' in message]
    )
    messages_per_week = Counter(
        [f"{datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S').isocalendar()[0]}-W{datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S').isocalendar()[1]:02d}" for message in messages if 'date' in message]
    )
    messages_per_weekday = Counter(
        [datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").strftime('%A') for message in messages if 'date' in message]
    )

    messages_per_hour = Counter(
        [datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").hour for message in messages if 'date' in message]
    )
    messages_per_month = Counter(
        [datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").strftime('%B') for message in messages if 'date' in message]
    )

    first_message_per_day = defaultdict(list)
    for message in messages:
        if 'date' in message:
            date = datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").date().isoformat()
            first_message_per_day[date].append(message)

    first_message_count = Counter()
    for date, msgs in first_message_per_day.items():
        first_message = min(msgs, key=lambda x: x['date'] if 'date' in x else float('inf'))
        if 'from' in first_message:
            first_message_count[first_message['from'] if first_message['from'] is not None else 'Unknown'] += 1

    user_message_counts = {('Unknown' if k is None else k): v for k, v in user_messages.items()}
    user_percentages = {('Unknown' if k is None else k): (v / total_messages) * 100 for k, v in user_messages.items()}

    average_messages_per_day = total_messages / len(messages_per_day) if messages_per_day else 0

    user_response_times = defaultdict(list)
    previous_message = None
    for message in messages:
        if previous_message and message.get('from') and previous_message.get('from') and message['from'] != previous_message['from']:
            time_difference = datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S") - datetime.strptime(previous_message['date'], "%Y-%m-%dT%H:%M:%S")
            if time_difference < timedelta(hours=1):
                user_response_times[previous_message['from'] if previous_message['from'] is not None else 'Unknown'].append(time_difference.total_seconds())
        previous_message = message if 'date' in message and 'from' in message else None
    
    average_response_times = {user: sum(times) / len(times) for user, times in user_response_times.items() if times}

    top_10_days = messages_per_day.most_common(10)

    statistics = {
        "total_messages": total_messages,
        "average_messages_per_day": average_messages_per_day,
        "average_response_times": average_response_times,
        "most_active_user": most_active_user,
        "user_message_counts": user_message_counts,
        "user_percentages": user_percentages,
        "word_frequencies": word_frequencies,
        "messages_per_day": dict(messages_per_day),
        "messages_per_week": dict(messages_per_week),
        "messages_per_weekday": dict(messages_per_weekday),
        "messages_per_hour": dict(messages_per_hour),
        "messages_per_month": dict(messages_per_month),
        "first_message_count": dict(first_message_count),
        "laugh_count": laugh_count,
        "top_10_days": top_10_days
    }

    logging.debug(f"Statistics: {statistics}")

    return statistics

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
