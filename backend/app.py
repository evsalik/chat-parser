import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
import logging
import numpy as np

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

logging.basicConfig(level=logging.DEBUG)

RUSSIAN_SWEARS = ['беспиздая', 'бля', 'блядва', 'блядиада', 'блядина', 'блядистость', 'блядки', 'блядовать', 'блядогон', 'блядословник', 'блядский', 'блядство', 'блядун', 'блядь', 'бляхомудия', 'взбляд', 'взъебнуть', 'взъебка', 'взъебывать', 'взъебщик', 'впиздить', 'впиздиться', 'впиздохать', 'впиздохивать', 'впиздохиваться', 'впиздронивать', 'впиздрониться', 'впиздюлить', 'впиздячил', 'впиздячить', 'впизживать', 'впизживаться', 'вхуйнуть', 'вхуйнуться', 'вхуяривание', 'вхуярить', 'выблядовал', 'выблядок', 'выебать', 'выебок', 'выебон', 'выёбывается', 'выпиздеться', 'выпиздить', 'выхуяривание', 'въебать', 'въебывать', 'глупизди', 'говноёб', 'голоёбица', 'греблядь', 'дерьмохеропиздократ', 'дерьмохеропиздократия', 'доебался', 'доебаться', 'доёбывать', 'долбоёб', 'допиздеться', 'дохуйнуть', 'дохуякать', 'дохуякивать', 'дохуяривавться', 'дураёб', 'дядёёб', 'ебалка', 'ебало', 'ебалово', 'ебальник', 'ебанатик', 'ебандеи', 'ебанёшься', 'ебанул', 'ебанулся', 'ебануть', 'ебануться', 'ебанутый', 'ебанько', 'ебаришка', 'ебаторий', 'ебаться', 'ебашит', 'ебеня', 'ебёт', 'ебистика', 'еблан', 'ебланить', 'ебливая', 'ебля', 'ебукентий', 'ёбака', 'ёбаный', 'ёбарь', 'ёбкость', 'ёбля', 'ёбнул', 'ёбнуться', 'ёбнутый', 'ёбс', 'заебал', 'заебать', 'заебись', 'заебцовый', 'заебенить', 'заёб', 'заёбанный', 'заебаться', 'запизденевать', 'запиздеть', 'запиздить', 'запизживаться', 'захуяривать', 'захуярить', 'злоебучая', 'изъебнулся', 'испиздился', 'испиздить', 'исхуячить', 'козлоёб', 'козлоёбина', 'козлоёбиться', 'козлоёбище', 'коноёбиться', 'косоёбится', 'многопиздная', 'мозгоёб', 'мудоёб', 'наблядовал', 'наебалово', 'наебать', 'наебаться', 'наебашился', 'наебениться', 'наебнулся', 'наебнуть', 'наёбка', 'нахуеверететь', 'нахуяривать', 'нахуяриться', 'напиздеть', 'напиздить', 'настоебать', 'невъебенный', 'нехуёвый', 'нехуй', 'оберблядь', 'объебал', 'объебалово', 'объебательство', 'объебать', 'объебаться', 'объебос', 'один хуй', 'однохуйственно', 'опизденевать', 'опиздихуительный', 'опиздоумел', 'оскотоёбился', 'остоебал', 'остопиздело', 'остопиздеть', 'остохуеть', 'отпиздить', 'отхуяривать', 'отъебаться', 'охуевать', 'охуенно', 'охуительный', 'охуенный', 'охуячивать', 'охуячить', 'переебать', 'перехуяривать', 'перехуярить', 'пёзды', 'пизда', 'пиздабол', 'пиздаёб', 'пиздакрыл', 'пиздануть', 'пиздануться', 'пиздатый', 'пизделиться', 'пизделякает', 'пиздеть', 'пиздец', 'пиздецкий', 'пиздёж', 'пиздёныш', 'пиздить', 'пиздобол', 'пиздоблошка', 'пиздобрат', 'пиздобратия', 'пиздовать', 'пиздовладелец', 'пиздодушие', 'пиздоёбищность', 'пиздолет', 'пиздолиз', 'пиздомания', 'пиздопляска', 'пиздорванец', 'пиздострадалец', 'пиздострадания', 'пиздохуй', 'пиздошить', 'пиздрик', 'пиздуй', 'пиздун', 'пиздюк', 'пиздюли', 'пиздюлина', 'пиздюлька', 'пиздюля', 'пиздюрить', 'пиздюхать', 'пиздюшник', 'подзаебать', 'подзаебенить', 'поднаебнуть', 'поднаебнуться', 'поднаёбывать', 'подпёздывать', 'подпиздывает', 'подъебнуть', 'подъёбка', 'подъёбки', 'подъёбывать', 'поебать', 'поебень', 'попиздеть', 'попиздили', 'похую', 'похуярили', 'приебаться', 'припиздеть', 'припиздить', 'прихуяривать', 'прихуярить', 'проблядь', 'проебать', 'проебаться', 'проёб', 'пропиздить', 'разъебай', 'разъебаться', 'разёбанный', 'распиздон', 'распиздошил', 'распиздяй', 'распиздяйство', 'расхуюжить', 'расхуяривать', 'скотоёб', 'скотоёбина', 'сосихуйский', 'спиздил', 'страхоеёбище', 'сухопиздая', 'схуярить', 'съебаться', 'трепездон', 'трепездонит', 'туебень', 'тупиздень', 'уебался', 'уебать', 'уёбище', 'уёбищенски', 'уёбок', 'уёбывать', 'упиздить', 'хитровыебанный', 'хуев', 'хуеватенький', 'хуевато', 'худоёбина', 'хуебратия', 'хуеглот', 'хуегрыз', 'хуедин', 'хуелес', 'хуеман', 'хуемырло', 'хуеплёт', 'хуепутало', 'хуесос', 'хуета', 'хуетень', 'хуёвина', 'хуёвничать', 'хуёво', 'хуёвый', 'хуила', 'хуйло', 'хуйнуть', 'хуйня', 'хуярить', 'хуяция', 'хули', 'хуя', 'хуяк', 'хуячить', 'шароёбиться']


def process_statistics(data):
    messages = data.get('messages', [])
    total_messages = len(messages)

    user_messages = Counter([message.get('from', 'Unknown') if message.get('from') is not None else 'Unknown' for message in messages if 'from' in message])
    most_active_user = user_messages.most_common(1)[0] if user_messages else ("N/A", 0)

    all_words = []
    laugh_count = 0
    message_lengths = []
    swear_count = 0
    swear_frequencies = Counter()
    messages_per_user_per_day = defaultdict(lambda: defaultdict(int))
    time_differences = []
    previous_message_time = None
    for message in messages:
        if 'text' in message:
            if isinstance(message['text'], list):
                text_content = ' '.join([part.get('text', '') for part in message['text'] if isinstance(part, dict) and 'text' in part])
            else:
                text_content = message['text']
            
            normalized_text = text_content.lower().replace('ё', 'е')
            
            words = re.findall(r'\b\w+\b', normalized_text)
            all_words.extend(words)
            message_length = len(normalized_text)
            if message_length > 0:
                message_lengths.append(message_length)

            if re.search(r'\b(ахах|хах|хаха|пазх|пах|ахзп|азпахз|апх|апз|аппа)\w*\b', normalized_text, re.IGNORECASE):
                laugh_count += 1

            for swear in RUSSIAN_SWEARS:
                if re.search(rf'(?<!\w){re.escape(swear)}(?!\w)', normalized_text, re.IGNORECASE):
                    swear_count += 1
                    swear_frequencies[swear] += 1

        if 'date' in message and 'from' in message:
            date = datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S").date().isoformat()
            user = message['from'] if message['from'] is not None else 'Unknown'
            messages_per_user_per_day[user][date] += 1

        if 'date' in message:
            current_message_time = datetime.strptime(message['date'], "%Y-%m-%dT%H:%M:%S")
            if previous_message_time is not None:
                time_difference = (current_message_time - previous_message_time).total_seconds()
                time_differences.append(time_difference)
            previous_message_time = current_message_time

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

    grouped_swear_frequencies = defaultdict(list)
    for swear, count in swear_frequencies.items():
        grouped_swear_frequencies[count].append(swear)
    sorted_grouped_swear_frequencies = sorted(grouped_swear_frequencies.items(), key=lambda x: x[0], reverse=True)

    suggested_swears = random.sample([swear for swear in RUSSIAN_SWEARS if swear not in swear_frequencies], 10)

    sticker_emoji_counts = Counter()
    for message in messages:
        if message.get('media_type') == 'sticker' and 'sticker_emoji' in message:
            sticker_emoji = message['sticker_emoji']
            sticker_emoji_counts[sticker_emoji] += 1

    voice_message_counts = Counter()
    for message in messages:
        if message.get('media_type') == 'voice_message' and 'from' in message:
            user = message['from'] if message['from'] is not None else 'Unknown'
            voice_message_counts[user] += 1
    
    video_message_counts = Counter()
    for message in messages:
        if message.get('media_type') == 'video_message' and 'from' in message:
            user = message['from'] if message['from'] is not None else 'Unknown'
            video_message_counts[user] += 1

    user_message_lengths = defaultdict(list)
    for message in messages:
        if 'from' in message and 'text' in message:
            user = message['from'] if message['from'] is not None else 'Unknown'
            if isinstance(message['text'], list):
                text_content = ' '.join([part.get('text', '') for part in message['text'] if isinstance(part, dict) and 'text' in part])
            else:
                text_content = message['text']
            message_length = len(text_content)
            user_message_lengths[user].append(message_length)

    continuation_delays = [delay for delay in time_differences if delay < 60 * 60]  # delays less than 60 minutes
    new_conversation_delays = [delay for delay in time_differences if delay >= 60 * 60]  # delays of 60 minutes or more

    if continuation_delays:
        continuation_mean = np.mean(continuation_delays)
    else:
        continuation_mean = 300  # default to 5 minutes

    if new_conversation_delays:
        new_conversation_mean = np.mean(new_conversation_delays)
    else:
        new_conversation_mean = 60 * 45  # default to 45 mins 

    conversations = []
    current_conversation = []
    for i, message in enumerate(messages):
        if i == 0:
            current_conversation.append(message)
        else:
            time_difference = time_differences[i - 1]
            if time_difference > 30 * continuation_mean:
                conversations.append(current_conversation)
                current_conversation = [message]
            else:
                current_conversation.append(message)
    if current_conversation:
        conversations.append(current_conversation)

    conversation_lengths = [len(conv) for conv in conversations]
    sorted_conversation_lengths = sorted(conversation_lengths, reverse=True)
    longest_conversation = max(conversation_lengths)

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
        "message_length_distribution": dict(Counter(message_lengths)),
        "top_10_days": top_10_days,
        "messages_per_user_per_day": {user: dict(counts) for user, counts in messages_per_user_per_day.items()},
        "swear_count": swear_count,
        "swear_frequencies": dict(swear_frequencies),
        "swear_rate": swear_count / total_messages * 100 if total_messages > 0 else 0,
        "sorted_grouped_swear_frequencies": sorted_grouped_swear_frequencies,
        "suggested_swears": suggested_swears,
        "sticker_emoji_counts": dict(sticker_emoji_counts),
        "voice_message_counts": dict(voice_message_counts),
        "video_message_counts": dict(video_message_counts),
        "user_message_lengths": {user: lengths for user, lengths in user_message_lengths.items()},
        "time_differences": time_differences,
        "conversations": len(conversations),
        "conversation_details": [{"start_time": conv[0]['date'], "end_time": conv[-1]['date'], "message_count": len(conv)} for conv in conversations],
        "sorted_conversation_lengths": sorted_conversation_lengths,
        "longest_conversation": longest_conversation
    }

    # logging.debug(f"Statistics: {statistics}")
    logging.debug(messages_per_user_per_day)

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
            logging.debug("started processing")
            statistics = process_statistics(data)
            logging.debug("completed processing")
        return jsonify(statistics)
    else:
        return jsonify({"error": "Invalid file format"}), 400

@app.route('/')
def hello():
    return "Backend is running"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)