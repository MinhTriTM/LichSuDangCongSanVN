import json
import os

input_file = r"d:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\tracnghiem\tracnghiem_LSD_chuong_gemini.json"
output_file = r"d:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\tracnghiem\output_qa.txt"

def main():
    print(f"Đang đọc file: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('questions', [])
        print(f"Tìm thấy {len(questions)} câu hỏi.")
        
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for q in questions:
                question = q.get('question', '').strip()
                answer = q.get('answer', '').strip()
                
                # Ghi ra file
                f_out.write(f"{question}\n")
                f_out.write(f"{answer}\n")
                
        print(f"Đã ghi thành công kết quả ra file: {output_file}")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()
