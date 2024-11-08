import json
from gtts import gTTS
from io import BytesIO
import pygame
import random

# Khởi tạo pygame
pygame.mixer.init()

# Đường dẫn tới file1
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
   pass
    # # # # Tạo âm thanh từ văn bản
    # tts = gTTS(text, lang=lang)
    # # # # Tạo một đối tượng BytesIO
    # mp3_fp = BytesIO()
    # # # # Lưu âm thanh vào đối tượng BytesIO
    # tts.write_to_fp(mp3_fp)
    # # # # Đặt lại vị trí của BytesIO về đầu
    # mp3_fp.seek(0)
    # # # # Khởi tạo pygame.mixer để phát âm thanh từ BytesIO1
    # pygame.mixer.music.load(mp3_fp, 'mp3')
    # pygame.mixer.music.play()

    # # # # Đợi đến khi âm thanh phát xong
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)

def update_json_files(data, completed):
    # Lưu lại file data.json
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Lưu lại file completed.json
    with open(completed_path, 'w', encoding='utf-8') as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

try:
    if choose == 1:
        while data:
            key, value = random.choice(list(data.items()))
            print(value, end='\t')
            #make answers
            count = 1
            answer_choose = [key]
            while count < 4:
                answer = random.choice(list(data.items()))[0]
                if answer not in answer_choose:
                    answer_choose.append(answer)
                    count += 1

            play_sound(value, lang='ko')
            while True:
                stop = input(': ')
                if stop == '2':
                    play_sound(value, lang='ko')
                else:
                    break

            random.shuffle(answer_choose)
            i = ord('a')
            for a in answer_choose:
                print(chr(i) + '\t', a)
                i += 1
            answer = input('enter your answer (a-d):')
            try:
                if answer_choose[ord(answer) - ord('a')] == key:
                    print('CORRECT')
                else:
                    print('NOT CORRECT')
                    print('Correct answer:', key)
                print('---------------------------\n')
            except:
                pass
            if stop == 's':
                break
            elif stop == '1':
                # Di chuyển phần tử từ data sang completed
                completed[key] = data.pop(key)
                update_json_files(data, completed)
                print('//')
    else:
        while data:
            key, value = random.choice(list(data.items()))
            print(key, end='\t')
           
            count = 1
            answer_choose = [value]
            while count < 4:
                answer = random.choice(list(data.items()))[1]
                if answer not in answer_choose:
                    answer_choose.append(answer)
                    count += 1

            play_sound(key, lang='en')
            while True:
                stop = input(': ')
                if stop == '2':
                    play_sound(key, lang='en')
                else:
                    break

            random.shuffle(answer_choose)
            i = ord('a')
            for a in answer_choose:
                print(chr(i) + '\t', a)
                i += 1
            answer = input('enter your answer (a-d):')
            try:
                if answer_choose[ord(answer) - ord('a')] == value:
                    print('CORRECT')
                else:
                    print('NOT CORRECT')
                    print('Correct answer:', value)
                print('---------------------------\n')
            except:
                pass
            play_sound(value, lang='ko')
            if stop == 'a':
                break
            elif stop == '1':
                # Di chuyển phần tử từ data sang completed
                completed[key] = data.pop(key)
                update_json_files(data, completed)
finally:
    # Cập nhật lại file json dù có ngoại lệ xảy ra
    update_json_files(data, completed)
