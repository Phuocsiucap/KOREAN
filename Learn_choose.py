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

# Bộ đếm số lần trả lời đúng liên tiếp
correct_count = {}

# Lựa chọn chế độ
print("Chọn cặp ngôn ngữ:")
print("1: Tiếng Hàn - Tiếng Anh")
print("2: Tiếng Anh - Tiếng Hàn")
print("3: Tiếng Việt - Tiếng hàn")
print("4: Tiếng Anh - Tiếng Việt")
choose = int(input("Nhập lựa chọn của bạn (1-4): "))

# Định nghĩa ngôn ngữ
language_map = {
    1: ('ko', 'en'),
    2: ('en', 'ko'),
    3: ('vi', 'ko'),
    4: ('en', 'vi')
}

source_lang, target_lang = language_map.get(choose, ('ko', 'en'))

def play_sound(text, lang):
    # Tạo âm thanh từ văn bản
    tts = gTTS(text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
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

try:
    while data:
        key, value = random.choice(list(data.items()))

        # Xác định từ và nghĩa theo cặp ngôn ngữ
        question = key if source_lang == 'en' else value
        answer = value if source_lang == 'en' else key

        print(question, end='\t')

        # Tạo các lựa chọn trả lời
        count = 1
        answer_choose = [answer]
        while count < 4:
            random_answer = random.choice(list(data.items()))[1 if source_lang == 'en' else 0]
            if random_answer not in answer_choose:
                answer_choose.append(random_answer)
                count += 1

        # Phát âm thanh câu hỏi
        play_sound(question, lang=source_lang)

        # Cho phép điều khiển bằng cách nhập '1' hoặc '2'
        while True:
            stop = input(': ')
            if stop == '2':
                play_sound(question, lang=source_lang)
            elif stop == '1':
                print(f"Chuyển từ '{key}' vào file completed.")
                completed[key] = data.pop(key)
                correct_count.pop(key, None)  # Xóa bộ đếm nếu có
                update_json_files(data, completed)
                break
            else:
                break

        # Nếu người dùng đã chọn '1', bỏ qua việc hỏi đáp án
        if stop == '1':
            continue

        # Hiển thị các lựa chọn
        random.shuffle(answer_choose)
        i = ord('a')
        for a in answer_choose:
            print(chr(i) + '\t', a)
            i += 1
        
        # Nhập câu trả lời từ người dùng
        answer_input = input('Nhập đáp án của bạn (a-d): ')
        try:
            if answer_choose[ord(answer_input) - ord('a')] == answer:
                print('CHÍNH XÁC')
                
                # Tăng số đếm đúng liên tiếp
                correct_count[key] = correct_count.get(key, 0) + 1
                
                # Nếu đúng 5 lần liên tiếp, chuyển từ sang completed
                if correct_count[key] >= 5:
                    print(f"Đã học xong từ: {key}")
                    completed[key] = data.pop(key)
                    correct_count.pop(key, None)  # Xóa bộ đếm của từ đã hoàn thành
            else:
                print('KHÔNG ĐÚNG')
                print('Đáp án đúng:', answer)
                
                # Đặt lại số đếm đúng liên tiếp về 0
                correct_count[key] = 0

            print('---------------------------\n')
        except:
            pass

        # Cập nhật file sau mỗi lần trả lời
        update_json_files(data, completed)

finally:
    # Cập nhật lại file json dù có ngoại lệ xảy ra
    update_json_files(data, completed)
