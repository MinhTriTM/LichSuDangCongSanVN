# Q17: Chuyển đổi PDF Giáo trình Lịch sử Đảng sang Markdown

**Câu hỏi:**
Hãy đọc nội dung file PDF sau và chuyển đổi hoàn toàn sang định dạng Markdown (.md). 
Đường dẫn file: "D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\GiaoTrinh_LSD.pdf"
Yêu cầu:
- Giữ nguyên cấu trúc, tiêu đề, các mục lục.
- Đảm bảo trích xuất đầy đủ văn bản.
- Lưu kết quả vào file: "D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\GiaoTrinh_LSD_PDF.md"
- Trả về thông báo khi hoàn tất.

**Suy nghĩ:**
- Sử dụng thư viện `pymupdf` (fitz) trong Python để trích xuất văn bản từ file PDF.
- Duyệt qua từng trang, lấy văn bản và định dạng sơ bộ sang Markdown.
- Lưu kết quả vào file đích được yêu cầu.

**Thao tác:**
1. Tạo script Python `convert_pdf_to_md.py`.
2. Thực thi script để chuyển đổi.
3. Kiểm tra file kết quả.
