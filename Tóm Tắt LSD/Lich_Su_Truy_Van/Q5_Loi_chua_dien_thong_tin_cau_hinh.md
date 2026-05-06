# Câu hỏi:
Người dùng chạy script và nhận được thông báo lỗi do chưa điền PROCESSOR_ID và cấu hình GCS Bucket.

# Suy nghĩ:
- Script đã chạy thành công nhưng dừng lại do cơ chế bảo vệ tôi viết sẵn.
- Người dùng cần mở file `convert_pdf_to_md.py` và sửa các biến `PROCESSOR_ID`, `GCS_INPUT_PREFIX`, `GCS_OUTPUT_URI`.
- Cần hướng dẫn họ làm sao để lấy những thông tin này từ Google Cloud Console (nếu họ chưa biết) hoặc đơn giản là nhắc họ vào file sửa.

# Câu trả lời:
Hướng dẫn chi tiết cách mở file và điền các thông tin cần thiết vào mã nguồn.