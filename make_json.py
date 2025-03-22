import json

def make_json(x_path):
    # Đường dẫn tới file
    file_path = x_path

    try:
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

        # Nhập đường dẫn file đầu ra từ người dùng
        output_path = r'D:\KOREAN\data.json'

        # Lưu dictionary vào file JSON
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Dictionary đã được lưu vào file {output_path}")

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file đầu vào.")
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

make_json(input('Enter address of file txt: '))
