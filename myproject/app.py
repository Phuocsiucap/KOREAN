from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from io import BytesIO
import pygame
import random
import json
import os

app = Flask(__name__)

# Khởi tạo pygame cho việc phát âm thanh
pygame.mixer.init()

# Đọc dữ liệu từ file JSON
data_path = 'D:/KOREAN/data.json'
completed_path = 'D:/KOREAN/completed_choose.json'

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Đọc file completed.json nếu có
try:
    with open(completed_path, 'r', encoding='utf-8') as f:
        completed = json.load(f)
except FileNotFoundError:
    completed = {}

# Chức năng phát âm thanh từ văn bản
def play_sound(text, lang='ko'):
    tts = gTTS(text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# API cho lựa chọn chế độ học
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_mode', methods=['POST'])
def choose_mode():
    mode = request.form['mode']
    if mode == '1':
        return render_template('choose_answer.html', mode='choose_answer')
    elif mode == '2':
        return render_template('write_answer.html', mode='write_answer')

@app.route('/get_question', methods=['GET'])
def get_question():
    mode = request.args.get('mode')
    if mode == 'choose_answer':
        key, value = random.choice(list(data.items()))
        # Tạo 4 đáp án ngẫu nhiên
        
        count = 1
        answers= [key]
        while count < 4:
            answer = random.choice(list(data.items()))[0]
            if answer not in answers:
                answers.append(answer)
                count += 1
        random.shuffle(answers)
        play_sound(value, lang='ko')
        return jsonify({'question': value, 'answers': answers, 'key': key})

    elif mode == 'write_answer':
        key, value = random.choice(list(data.items()))
        play_sound(value, lang='ko')
        return jsonify({'question': value, 'key': key})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    answer = request.form['answer']
    mode = request.form['mode']
    key = request.form['key']
    if mode == 'choose_answer':
        correct = 'CORRECT' if answer == key else 'NOT CORRECT'
        if correct == 'CORRECT':
            completed[key] = data.pop(key)
        return jsonify({'result': correct})

    elif mode == 'write_answer':
        correct = 'CORRECT' if answer.strip().lower() == key.strip().lower() else 'NOT CORRECT'
        if correct == 'CORRECT':
            completed[key] = data.pop(key)
        return jsonify({'result': correct})

    return jsonify({'result': 'Error'})

# Cập nhật các file JSON
def update_json_files():
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(completed_path, 'w', encoding='utf-8') as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

# Đảm bảo cập nhật lại dữ liệu trước khi kết thúc
@app.before_request
def ensure_update():
    update_json_files()

if __name__ == '__main__':
    app.run(debug=True)
