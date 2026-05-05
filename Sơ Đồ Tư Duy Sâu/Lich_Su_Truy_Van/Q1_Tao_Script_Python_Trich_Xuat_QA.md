# Câu hỏi:
viết html chỉ xem đáp án đúng@[d:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\tracnghiem\tracnghiem_LSD_chuong_gemini.json]
viết thêm file python nhận input từ @[d:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\tracnghiem\tracnghiem_LSD_chuong_gemini.json] 
thực hiện cho ra output:
line 1: question
line 2: answer
line 3: question
line 4: answer

# Suy nghĩ (Thinking):
- Người dùng muốn trích xuất dữ liệu từ file json có sẵn, theo định dạng question và answer nối tiếp nhau ở mỗi dòng.
- Sẽ sử dụng Python với thư viện `json` để đọc file đầu vào.
- Sau khi duyệt qua list `questions`, trích xuất `question` và `answer`, rồi ghi lần lượt từng cái ra một dòng trong file txt.

# Câu trả lời:
Tôi đã tạo một script Python (`extract_qa.py`) để đọc dữ liệu từ file JSON và ghi nội dung câu hỏi và đáp án ra file text mới. Mỗi câu hỏi ở một dòng và đáp án tương ứng nằm ngay dòng tiếp theo.
