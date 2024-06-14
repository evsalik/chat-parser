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

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

logging.basicConfig(level=logging.DEBUG)

RUSSIAN_SWEARS = ['беспиздая', 'бля', 'блядва', 'блядиада', 'блядина', 'блядистость', 'блядки', 'блядовать', 'блядогон', 'блядословник', 'блядский', 'блядство', 'блядун', 'блядь', 'бляхомудия', 'взбляд', 'взъебнуть', 'взъебка', 'взъебывать', 'взъебщик', 'впиздить', 'впиздиться', 'впиздохать', 'впиздохивать', 'впиздохиваться', 'впиздронивать', 'впиздрониться', 'впиздюлить', 'впиздячил', 'впиздячить', 'впизживать', 'впизживаться', 'вхуйнуть', 'вхуйнуться', 'вхуяривание', 'вхуярить', 'выблядовал', 'выблядок', 'выебать', 'выебок', 'выебон', 'выёбывается', 'выпиздеться', 'выпиздить', 'выхуяривание', 'въебать', 'въебывать', 'глупизди', 'говноёб', 'голоёбица', 'греблядь', 'дерьмохеропиздократ', 'дерьмохеропиздократия', 'доебался', 'доебаться', 'доёбывать', 'долбоёб', 'допиздеться', 'дохуйнуть', 'дохуякать', 'дохуякивать', 'дохуяривавться', 'дураёб', 'дядёёб', 'ебалка', 'ебало', 'ебалово', 'ебальник', 'ебанатик', 'ебандеи', 'ебанёшься', 'ебанул', 'ебанулся', 'ебануть', 'ебануться', 'ебанутый', 'ебанько', 'ебаришка', 'ебаторий', 'ебаться', 'ебашит', 'ебеня', 'ебёт', 'ебистика', 'еблан', 'ебланить', 'ебливая', 'ебля', 'ебукентий', 'ёбака', 'ёбаный', 'ёбарь', 'ёбкость', 'ёбля', 'ёбнул', 'ёбнуться', 'ёбнутый', 'ёбс', 'жидоёб', 'жидоёбка', 'жидоёбский', 'заебал', 'заебать', 'заебись', 'заебцовый', 'заебенить', 'заёб', 'заёбанный', 'заебаться', 'запизденевать', 'запиздеть', 'запиздить', 'запизживаться', 'захуяривать', 'захуярить', 'злоебучая', 'изъебнулся', 'испиздился', 'испиздить', 'исхуячить', 'козлоёб', 'козлоёбина', 'козлоёбиться', 'козлоёбище', 'коноёбиться', 'косоёбится', 'многопиздная', 'мозгоёб', 'мудоёб', 'наблядовал', 'наебалово', 'наебать', 'наебаться', 'наебашился', 'наебениться', 'наебнулся', 'наебнуть', 'наёбка', 'нахуеверететь', 'нахуяривать', 'нахуяриться', 'напиздеть', 'напиздить', 'настоебать', 'невъебенный', 'нехуёвый', 'нехуй', 'оберблядь', 'объебал', 'объебалово', 'объебательство', 'объебать', 'объебаться', 'объебос', 'один хуй', 'однохуйственно', 'опизденевать', 'опиздихуительный', 'опиздоумел', 'оскотоёбился', 'остоебал', 'остопиздело', 'остопиздеть', 'остохуеть', 'отпиздить', 'отхуяривать', 'отъебаться', 'охуевать', 'охуенно', 'охуительный', 'охуенный', 'охуячивать', 'охуячить', 'переебать', 'перехуяривать', 'перехуярить', 'пёзды', 'пизда', 'пиздабол', 'пиздаёб', 'пиздакрыл', 'пиздануть', 'пиздануться', 'пиздатый', 'пизделиться', 'пизделякает', 'пиздеть', 'пиздец', 'пиздецкий', 'пиздёж', 'пиздёныш', 'пиздить', 'пиздобол', 'пиздоблошка', 'пиздобрат', 'пиздобратия', 'пиздовать', 'пиздовладелец', 'пиздодушие', 'пиздоёбищность', 'пиздолет', 'пиздолиз', 'пиздомания', 'пиздопляска', 'пиздорванец', 'пиздострадалец', 'пиздострадания', 'пиздохуй', 'пиздошить', 'пиздрик', 'пиздуй', 'пиздун', 'пиздюк', 'пиздюли', 'пиздюлина', 'пиздюлька', 'пиздюля', 'пиздюрить', 'пиздюхать', 'пиздюшник', 'подзаебать', 'подзаебенить', 'поднаебнуть', 'поднаебнуться', 'поднаёбывать', 'подпёздывать', 'подпиздывает', 'подъебнуть', 'подъёбка', 'подъёбки', 'подъёбывать', 'поебать', 'поебень', 'попиздеть', 'попиздили', 'похую', 'похуярили', 'приебаться', 'припиздеть', 'припиздить', 'прихуяривать', 'прихуярить', 'проблядь', 'проебать', 'проебаться', 'проёб', 'пропиздить', 'разъебай', 'разъебаться', 'разёбанный', 'распиздон', 'распиздошил', 'распиздяй', 'распиздяйство', 'расхуюжить', 'расхуяривать', 'скотоёб', 'скотоёбина', 'сосихуйский', 'спиздил', 'страхоеёбище', 'сухопиздая', 'схуярить', 'съебаться', 'трепездон', 'трепездонит', 'туебень', 'тупиздень', 'уебался', 'уебать', 'уёбище', 'уёбищенски', 'уёбок', 'уёбывать', 'упиздить', 'хитровыебанный', 'хуев', 'хуеватенький', 'хуевато', 'худоёбина', 'хуебратия', 'хуеглот', 'хуегрыз', 'хуедин', 'хуелес', 'хуеман', 'хуемырло', 'хуеплёт', 'хуепутало', 'хуесос', 'хуета', 'хуетень', 'хуёвина', 'хуёвничать', 'хуёво', 'хуёвый', 'хуила', 'хуйло', 'хуйнуть', 'хуйня', 'хуярить', 'хуяция', 'хули', 'хуя', 'хуяк', 'хуячить', 'шароёбиться']


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
    for message in messages:
        if 'text' in message:
            if isinstance(message['text'], list):
                text_content = ' '.join([part.get('text', '') for part in message['text'] if isinstance(part, dict) and 'text' in part])
            else:
                text_content = message['text']
            
            # Normalize text
            normalized_text = text_content.lower().replace('ё', 'е')
            
            words = re.findall(r'\b\w+\b', normalized_text)
            all_words.extend(words)
            message_length = len(normalized_text)
            if message_length > 0:  # Filter out messages with 0 characters
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
        "suggested_swears": suggested_swears
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
