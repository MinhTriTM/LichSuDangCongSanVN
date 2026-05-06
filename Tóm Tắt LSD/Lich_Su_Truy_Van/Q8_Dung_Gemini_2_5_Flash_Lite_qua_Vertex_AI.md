# Câu hỏi:
Người dùng muốn sử dụng Gemini 2.5 Flash-Lite thông qua Vertex AI và Google Cloud CLI để thay thế cho Document AI OCR.

# Suy nghĩ:
- Mô hình `gemini-2.5-flash-lite-preview-09-2025` hỗ trợ PDF cực tốt, lên đến 1000 trang / 50MB. Tuy nhiên, nếu file PDF > 7MB thì bắt buộc phải đưa lên GCS trước khi gọi API của Vertex AI.
- Do các giáo trình thường lớn, tôi đã viết một script tự động: Upload PDF lên GCS -> Gọi Vertex AI đọc PDF từ GCS -> Sinh Markdown -> Xóa file tạm trên GCS.
- Cần cung cấp mã nguồn này và hướng dẫn người dùng cài đặt thêm thư viện `google-cloud-aiplatform` (Vertex AI SDK) nếu chưa có.
- Ghi lại log tương tác vào thư mục `Lich_Su_Truy_Van`.

# Câu trả lời:
Hướng dẫn chi tiết cách chạy script `convert_pdf_to_md_gemini.py` vừa tạo, cũng như cách cài đặt thư viện cần thiết.