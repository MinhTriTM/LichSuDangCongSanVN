import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# ==============================================================================
# CẤU HÌNH DỰ ÁN
# ==============================================================================
PROJECT_ID = "tool-dich-thuat"
LOCATION = "us-central1" # Vertex AI hỗ trợ tốt nhất ở us-central1
MODEL_ID = "gemini-2.5-flash"

# Danh sách các file cục bộ
PDF_FILES = [
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\giao-trinh-lich-su-dang-cong-san-viet-nam-bo-gddt-ctqg-2021.pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\Đề cương - LỊCH SỬ ĐẢNG CSVN (2025) -.pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\GiaoTrinh_LSD.pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\Tóm tắt kiến thức Lịch Sử Đảng.pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\[LSĐ] - TỔNG HỢP KIẾN THỨC LỊCH SỬ ĐẢNG CỘNG SẢN VIỆT NAM.pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\Tóm tắt lý thuyết Lịch sử Đảng Cộng sản Việt Nam (LSĐ).pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\Tổng hợp kiến thức giáo trình lịch sử đảng.pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\NOI DUNG ON TAP MON LSD - Tài liệu tham khảo môn học.pdf",
    r"D:\Download\Thi\LSD\Tóm Tắt LSD\Tong hop kien thuc giao trinh lich su dang.pdf"
]

def main():
    # Khởi tạo Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_ID)
    
    prompt = """
    Bạn là một chuyên gia số hóa tài liệu. Hãy đọc toàn bộ nội dung tài liệu PDF này 
    và chuyển đổi toàn bộ sang định dạng Markdown. 
    Yêu cầu:
    - Giữ nguyên cấu trúc tiêu đề (Heading 1, 2, 3...).
    - Trình bày rõ ràng các đoạn văn, danh sách (list) và bảng biểu (table) nếu có.
    - Trích xuất toàn bộ văn bản một cách chính xác nhất.
    """

    for pdf_path in PDF_FILES:
        filename = os.path.basename(pdf_path)
        
        try:
            print(f"Đang đọc file {filename} từ máy tính...")
            # Đọc file PDF trực tiếp dưới dạng byte
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            
            # Đưa dữ liệu trực tiếp vào Part (Inline Data)
            pdf_part = Part.from_data(data=pdf_data, mime_type="application/pdf")
            
            print(f"Đang nhờ Gemini 2.5 Flash-Lite xử lý {filename}...")
            # Sử dụng generation_config để tối đa hóa token đầu ra (65535 cho bản Flash-Lite)
            response = model.generate_content(
                [pdf_part, prompt],
                generation_config={"max_output_tokens": 65535}
            )
            
            # Lưu kết quả ra file Markdown
            md_path = pdf_path.replace(".pdf", ".md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(response.text)
                
            print(f"✅ Đã xử lý và lưu thành công: {md_path}\n")
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {filename}: {e}\n")
            print("Ghi ý: Nếu lỗi do dung lượng file vượt quá giới hạn Inline Data (khoảng 7MB-20MB tuỳ request), bạn bắt buộc phải dùng Google Cloud Storage.")

if __name__ == "__main__":
    main()
