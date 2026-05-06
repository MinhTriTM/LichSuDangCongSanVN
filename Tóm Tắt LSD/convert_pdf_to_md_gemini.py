import os
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# ==============================================================================
# CẤU HÌNH DỰ ÁN
# ==============================================================================
PROJECT_ID = "tool-dich-thuat"
LOCATION = "us-central1" # Vertex AI hỗ trợ tốt nhất ở us-central1
MODEL_ID = "gemini-2.5-flash-lite-preview-09-2025"
BUCKET_NAME = "YOUR_BUCKET_NAME" # BẮT BUỘC: Nhập tên Bucket GCS của bạn vào đây

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

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Tải file PDF cục bộ lên Google Cloud Storage (Do file to > 7MB cần qua GCS)"""
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    print(f"Đang tải {os.path.basename(source_file_name)} lên GCS...")
    blob.upload_from_filename(source_file_name)
    return f"gs://{bucket_name}/{destination_blob_name}"

def delete_from_gcs(bucket_name, blob_name):
    """Xóa file tạm trên GCS sau khi xử lý xong"""
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

def main():
    if "YOUR_BUCKET_NAME" in BUCKET_NAME:
        print("LỖI: Bạn chưa điền BUCKET_NAME trong file code. Vui lòng mở file và sửa dòng số 11.")
        return

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
        blob_name = f"gemini_temp/{filename}"
        
        try:
            # 1. Tải PDF lên GCS
            gcs_uri = upload_to_gcs(BUCKET_NAME, pdf_path, blob_name)
            
            # 2. Đọc file từ GCS đưa vào Gemini
            pdf_part = Part.from_uri(uri=gcs_uri, mime_type="application/pdf")
            
            print(f"Đang nhờ Gemini 2.5 Flash-Lite xử lý {filename}...")
            # Sử dụng generation_config để tối đa hóa token đầu ra (65535 cho bản Flash-Lite)
            response = model.generate_content(
                [pdf_part, prompt],
                generation_config={"max_output_tokens": 65535}
            )
            
            # 3. Lưu kết quả ra file Markdown
            md_path = pdf_path.replace(".pdf", ".md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(response.text)
                
            print(f"✅ Đã xử lý và lưu thành công: {md_path}\n")
            
            # (Tùy chọn) 4. Xóa file trên GCS để dọn dẹp không gian
            delete_from_gcs(BUCKET_NAME, blob_name)
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {filename}: {e}\n")

if __name__ == "__main__":
    main()
