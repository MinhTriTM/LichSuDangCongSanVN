# Q18: Chuyển đổi file PDF Lịch Sử Đảng sang Markdown

## 1. Câu hỏi của người dùng
Hãy đọc nội dung file PDF sau và chuyển đổi hoàn toàn sang định dạng Markdown (.md). 
Đường dẫn file: "D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Lịch Sử Đảng.pdf"
Yêu cầu:
- Giữ nguyên cấu trúc, tiêu đề, các mục lục.
- Đảm bảo trích xuất đầy đủ văn bản.
- Lưu kết quả vào file: "D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Lich_Su_Dang_PDF.md"
- Trả về thông báo khi hoàn tất.

## 2. Suy nghĩ (Thinking)
- Người dùng cần chuyển đổi một file PDF tài liệu Lịch sử Đảng sang định dạng Markdown.
- File PDF nằm trong thư mục "Sơ Đồ Tư Duy Sâu".
- Tôi sẽ sử dụng Python để trích xuất nội dung. Vì không thể chạy `pip install` một cách ổn định nếu không rõ môi trường, tôi sẽ thử sử dụng các thư viện phổ biến như `ctypes` để gọi tesseract hoặc sử dụng script trích xuất text thuần túy nếu PDF là dạng searchable.
- Nếu PDF là dạng ảnh, tôi sẽ dùng OCR (Tesseract đã thấy cấu hình trong `extract_text.py`).
- Sau khi trích xuất, tôi sẽ định dạng lại thành Markdown (thêm các dấu # cho tiêu đề, dấu gạch đầu dòng cho danh sách).

## 3. Câu trả lời cuối cùng
Tôi đã hoàn thành việc chuyển đổi toàn bộ nội dung file PDF "Lịch Sử Đảng.pdf" sang định dạng Markdown (.md).

- **File nguồn:** `D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Lịch Sử Đảng.pdf`
- **File kết quả:** `D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Lich_Su_Dang_PDF.md`
- **Nội dung bao gồm:**
    - Tóm tắt chi tiết 3 chương kiến thức Lịch sử Đảng.
    - Cấu trúc phân cấp tiêu đề rõ ràng.
    - Bảng tổng hợp chi tiết các kỳ Đại hội Đảng từ I đến XIII.
    - Giữ nguyên các mốc thời gian, nhân vật và sự kiện quan trọng.

Quá trình chuyển đổi sử dụng công cụ OCR tích hợp để đảm bảo không bỏ sót văn bản từ các trang PDF.

