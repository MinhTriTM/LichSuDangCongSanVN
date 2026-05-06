import os
import re
from typing import Optional
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud import storage

# ==============================================================================
# CẤU HÌNH DỰ ÁN
# ==============================================================================
PROJECT_ID = "tool-dich-thuat"
LOCATION = "us" # hoặc "eu"
PROCESSOR_ID = "YOUR_PROCESSOR_ID" # Thay bằng ID của Enterprise Document OCR
GCS_INPUT_PREFIX = "gs://YOUR_BUCKET_NAME/input_pdfs/" # Thư mục chứa PDF trên GCS
GCS_OUTPUT_URI = "gs://YOUR_BUCKET_NAME/output_json/"  # Thư mục lưu kết quả

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

def batch_process_documents(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
    gcs_output_uri: str,
    timeout: int = 1200,
):
    """
    Sử dụng Batch Processing cho các tài liệu dài (>15 trang).
    """
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    )

    name = client.processor_path(project_id, location, processor_id)

    # Cấu hình GCS input
    gcs_document = documentai.GcsDocument(
        gcs_uri=gcs_input_uri, mime_type="application/pdf"
    )
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

    # Cấu hình GCS output
    gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=gcs_output_uri
    )
    output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

    request = documentai.BatchProcessRequest(
        name=name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    print(f"Đang gửi yêu cầu xử lý hàng loạt cho: {gcs_input_uri}")
    operation = client.batch_process_documents(request=request)

    print("Đang chờ quá trình xử lý hoàn tất (có thể mất vài phút)...")
    try:
        operation.result(timeout=timeout)
        print("Xử lý hoàn tất!")
    except Exception as e:
        print(f"Lỗi hoặc quá thời gian chờ: {e}")

    # Lấy thông tin metadata
    metadata = documentai.BatchProcessMetadata(operation.metadata)
    if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
        print(f"Quá trình xử lý không thành công hoàn toàn. Trạng thái: {metadata.state}")

    return metadata

def download_and_convert_to_markdown(gcs_output_uri: str, original_filename: str):
    """
    Tải file JSON từ GCS về, ghép các shard và chuyển thành Markdown.
    """
    # GCS_OUTPUT_URI thường có dạng gs://bucket/path/to/output/
    # Khi xử lý xong, Document AI sẽ tạo thêm một thư mục chứa ID operation.
    match = re.match(r"gs://([^/]+)/(.*)", gcs_output_uri)
    if not match:
        print("Đường dẫn GCS Output không hợp lệ.")
        return

    bucket_name = match.group(1)
    prefix = match.group(2)

    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(bucket_name)

    # Tìm các file JSON kết quả
    blobs = bucket.list_blobs(prefix=prefix)
    
    full_text = ""
    json_files = [blob for blob in blobs if blob.name.endswith(".json")]
    
    # Do tài liệu dài sẽ bị chia thành nhiều "shard" (mỗi shard 20 trang)
    # Cần sort theo số shard (nếu có)
    json_files.sort(key=lambda x: x.name)

    print(f"Tìm thấy {len(json_files)} file JSON kết quả. Đang kết hợp...")

    for blob in json_files:
        json_string = blob.download_as_bytes()
        document = documentai.Document.from_json(json_string, ignore_unknown_fields=True)
        full_text += document.text + "\n\n"

    # Lưu ra file Markdown cục bộ
    md_filename = os.path.basename(original_filename).replace(".pdf", ".md")
    output_path = os.path.join(os.path.dirname(original_filename), md_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"Đã lưu nội dung thành công tại: {output_path}\n")

def main():
    if "YOUR_PROCESSOR_ID" in PROCESSOR_ID or "YOUR_BUCKET_NAME" in GCS_INPUT_PREFIX:
        print("LỖI: Bạn cần điền đầy đủ PROCESSOR_ID và cấu hình GCS Bucket trong script.")
        print("Mở file convert_pdf_to_md.py và điền thông tin trước khi chạy.")
        return

    # Lưu ý: Script này giả định bạn ĐÃ UPLOAD các file PDF lên bucket GCS_INPUT_PREFIX.
    # Chạy lần lượt từng file (hoặc cấu hình Batch Documents để chạy 1 lượt)
    
    for local_path in PDF_FILES:
        filename = os.path.basename(local_path)
        gcs_input_uri = os.path.join(GCS_INPUT_PREFIX, filename).replace("\\", "/")
        
        # Đường dẫn thư mục output riêng cho từng file
        file_output_uri = os.path.join(GCS_OUTPUT_URI, filename.replace(".pdf", "")) + "/"
        file_output_uri = file_output_uri.replace("\\", "/")
        
        try:
            # 1. Gọi Batch Processing (Tài liệu phải nằm trên Google Cloud Storage)
            batch_process_documents(
                project_id=PROJECT_ID,
                location=LOCATION,
                processor_id=PROCESSOR_ID,
                gcs_input_uri=gcs_input_uri,
                gcs_output_uri=file_output_uri
            )
            
            # 2. Lấy dữ liệu từ Bucket Output và ghi ra file Markdown
            download_and_convert_to_markdown(file_output_uri, local_path)
            
        except Exception as e:
            print(f"Đã xảy ra lỗi khi xử lý {filename}: {e}")

if __name__ == "__main__":
    main()
