import json
from gtts import gTTS
from io import BytesIO
import pygame
import random

# Khởi tạo pygame
pygame.mixer.init()

# Đường dẫn tới file
data_path = r'D:\KOREAN\data.json'

# Chọn đường dẫn để lưu kết quả
completed_path = input("Nhập đường dẫn để lưu kết quả (ví dụ: D:\\KOREAN\\co_ban2.json): ")

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
print('Chọn chế độ:')
print('1: Korean - English')
print('2: English - Korean')
print('3: Vietnamese - English')
print('4: English - Vietnamese')
print('5: Korean - Vietnamese')
print('6: Vietnamese - Korean')
choose = int(input('Nhập lựa chọn của bạn (1-6): '))

def play_sound(text, lang='ko'):
    # Tạo âm thanh từ văn bản
    tts = gTTS(text, lang=lang)
    # Tạo một đối tượng BytesIO
    mp3_fp = BytesIO()
    # Lưu âm thanh vào đối tượng BytesIO
    tts.write_to_fp(mp3_fp)
    # Đặt lại vị trí của BytesIO về đầu
    mp3_fp.seek(0)
    # Khởi tạo pygame.mixer để phát âm thanh từ BytesIO
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()

    # Đợi đến khi âm thanh phát xong
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def update_json_files(data, completed):
    # Lưu lại file data.json
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Lưu lại file completed.json
    with open(completed_path, 'w', encoding='utf-8') as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

# Chọn ngôn ngữ dựa trên lựa chọn
language_map = {
    1: ('ko', 'en'),    # Korean - English
    2: ('en', 'ko'),    # English - Korean
    3: ('vi', 'en'),    # Vietnamese - English
    4: ('en', 'vi'),    # English - Vietnamese
    5: ('ko', 'vi'),    # Korean - Vietnamese
    6: ('vi', 'ko')     # Vietnamese - Korean
}

source_lang, target_lang = language_map.get(choose, ('ko', 'en'))  # Mặc định là Korean - English

# Chuyển dữ liệu về thứ tự cố định
def reorder_data(data, source_lang, target_lang):
    reordered_data = {}
    
    for key, value in data.items():
        if source_lang == 'ko':  # Nếu ngôn ngữ nguồn là tiếng Hàn
            # Tiếng Hàn luôn là value
            if target_lang == 'en':  # Korean -> English
                reordered_data[value] = key
            elif target_lang == 'vi':  # Korean -> Vietnamese
                reordered_data[key] = value
        elif source_lang == 'en':  # Nếu ngôn ngữ nguồn là tiếng Anh
            # Tiếng Anh luôn là key
            if target_lang == 'ko':  # English -> Korean
                reordered_data[key] = value
            elif target_lang == 'vi':  # English -> Vietnamese
                reordered_data[value] = key
        elif source_lang == 'vi':  # Nếu ngôn ngữ nguồn là tiếng Việt
            if target_lang == 'en':  # Vietnamese -> English
                reordered_data[value] = key
            elif target_lang == 'ko':  # Vietnamese -> Korean
                reordered_data[value] =  key
    return reordered_data

# Cập nhật lại dữ liệu với thứ tự cố định
data = reorder_data(data, source_lang, target_lang)

# Hàm so sánh không phân biệt chữ hoa chữ thường
def compare_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.strip().lower()

try:
    consecutive_correct = {}  # Số lần trả lời đúng liên tiếp cho từng từ

    while data:
        key, value = random.choice(list(data.items()))
        print(value, end='\t')
        play_sound(value, lang=source_lang)  # Phát âm theo ngôn ngữ nguồn
        while True:
            stop = input(': ')
            if stop == '2':
                play_sound(value, lang=source_lang)
            else:
                break
        answer = input('Enter answer: ')
        play_sound(key, lang=target_lang)  # Phát âm theo ngôn ngữ đích

        # Kiểm tra trả lời và cập nhật số lần trả lời đúng liên tiếp
        if not compare_answer(answer, key):
            print(key)
            consecutive_correct[key] = 0  # Sai thì đặt lại đếm cho từ này
        else:
            if key not in consecutive_correct:
                consecutive_correct[key] = 0
            consecutive_correct[key] += 1  # Đúng thì tăng đếm

        print('---------------------------\n')

        # Nếu đúng 5 lần liên tiếp, chuyển từ đó sang file completed
        if consecutive_correct[key] == 2:
            print(f"Đã đúng 5 lần liên tiếp cho từ {key}, chuyển sang file completed.")
            completed[key] = data.pop(key)
            update_json_files(data, completed)
            consecutive_correct[key] = 0  # Đặt lại đếm sau khi chuyển sang file completed

        if stop == 'a':
            break
        elif stop == '1':
            # Di chuyển phần tử từ data sang completed
            completed[key] = data.pop(key)
            update_json_files(data, completed)

finally:
    # Cập nhật lại file json dù có ngoại lệ xảy ra
    update_json_files(data, completed)
