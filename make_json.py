import json

def make_json(x_path):
    # Đường dẫn tới file
    file_path = x_path

    # Đọc dữ liệu từ file.txt
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = {}
    for line in lines:
        line = line.strip()
        if ':' in line:
            # Tách các từ bằng dấu ':'
            english_word, korean_word = line.split(':', maxsplit=1)
            # Xóa bỏ khoảng trắng thừa
            data[english_word.strip()] = korean_word.strip()

    # Lưu dictionary vào file JSON
    output_path = r'D:\KOREAN\data.json'
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Dictionary đã được lưu vào file data.json")

make_json(input('enter address of file txt: '))