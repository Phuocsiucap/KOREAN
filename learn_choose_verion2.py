import json
from gtts import gTTS
from io import BytesIO
import pygame
import random
from langdetect import detect

# Khởi tạo pygame
pygame.mixer.init()

# Đường dẫn tới file
data_path = r'D:\KOREAN\data.json'
completed_path = r'D:\KOREAN\co_ban2.json'

# Đọc file data.json
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Đọc file completed.json hoặc khởi tạo nếu chưa có
try:
    with open(completed_path, 'r', encoding='utf-8') as f:
        completed = json.load(f)
except FileNotFoundError:
    completed = {}

# Lựa chọn chế độ
choose = int(input('1: Korean - English\n2: English - Korean\nEnter choice: '))

def play_sound(text, lang='ko'):
    try:
        lang = detect(text)
        if lang not in ['ko', 'en', 'vi']:
            lang = 'en'
    except:
        lang = 'en'
    
    tts = gTTS(text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def update_json_files(data, completed):
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open(completed_path, 'w', encoding='utf-8') as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

try:
    while data:
        key, value = random.choice(list(data.items()))
        # Tạo danh sách đáp án
        answer_list = [key] if choose == 1 else [value]
        while len(answer_list) < 4:
            answer = random.choice(list(data.items()))[0 if choose == 1 else 1]
            if answer not in answer_list:
                answer_list.append(answer)

        question = value if choose == 1 else key
        print(question, end='\t')
        play_sound(question)
        while True:
            stop = input(': ')
            if stop == '2':
                play_sound(value, lang='ko')
            else:
                break

        #Xáo trộn danh sách đáp án và phát âm từng đáp án
        random.shuffle(answer_list)
        answer_dict = {}
        i = ord('a')
        for ans in answer_list:
            option = chr(i)
            answer_dict[option] = ans
            print(f"{option}. {ans}")
            play_sound(ans)
            i += 1

        # Người dùng chọn đáp án
        answer = input('Enter your answer (a-d): ')
        try:
            correct_answer = key if choose == 1 else value
            if answer_dict[answer] == correct_answer:
                print('CORRECT')
            else:
                print('NOT CORRECT')
                print('Correct answer:', correct_answer)
                play_sound("Đáp án đúng là " + correct_answer)
            print('---------------------------\n')
        except:
            print("Invalid input. Please try again.")
        if stop == 's':
            break
        elif stop == '1':
            completed[key] = data.pop(key)
            update_json_files(data, completed)
            print('//')
finally:
    update_json_files(data, completed)