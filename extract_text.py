import subprocess
import os

# --- Cấu hình ---
# Đảm bảo đường dẫn này TRÍCH XÁC tới file tesseract.exe trên máy của bạn.
# Dựa trên thông tin bạn cung cấp, đường dẫn này là: C:	ools\Tesseract-OCR	esseract.exe
TESSERACT_PATH = r"C:\tools\Tesseract-OCR\tesseract.exe"

# Đường dẫn tới thư mục chứa các file ảnh bài trắc nghiệm của bạn.
IMAGES_DIR = r"D:\Download\Thi\LSD\BÀI TRẮC NGHIỆM LSĐ"

# Tên file đầu ra sẽ chứa tất cả văn bản đã trích xuất.
OUTPUT_TEXT_FILE = "extracted_text_from_images.txt"

# --- Kiểm tra xem Tesseract.exe có tồn tại không ---
if not os.path.exists(TESSERACT_PATH):
    print(f"Lỗi: Không tìm thấy tesseract.exe tại đường dẫn: {TESSERACT_PATH}")
    print("Vui lòng kiểm tra lại biến TESSERACT_PATH trong script và chỉnh sửa cho đúng.")
    exit()

# --- Xử lý các file ảnh ---
extracted_texts = []
# Lấy danh sách các file ảnh trong thư mục
# Đảm bảo bạn chỉ lấy các file có đuôi .jpg, .jpeg, .png, .gif, .bmp
image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

if not image_files:
    print(f"Không tìm thấy file ảnh nào trong thư mục: {IMAGES_DIR}")
    exit()

print(f"Tìm thấy {len(image_files)} file ảnh. Đang tiến hành trích xuất văn bản...")

# Sắp xếp các file ảnh theo tên để xử lý theo thứ tự
for image_file in sorted(image_files):
    image_path = os.path.join(IMAGES_DIR, image_file)
    print(f"Đang xử lý ảnh: {image_file}")

    try:
        # Xây dựng lệnh Tesseract
        command = [
            TESSERACT_PATH,
            image_path,
            "stdout",  # Yêu cầu Tesseract xuất kết quả ra stdout
            "-l", "vie" # Sử dụng gói ngôn ngữ tiếng Việt
        ]

        # Thực thi lệnh và bắt kết quả
        # text=True và encoding='utf-8' để xử lý văn bản tiếng Việt đúng cách
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            # Thêm phần đánh dấu để biết văn bản này từ ảnh nào
            extracted_texts.append(f"\n--- BẮT ĐẦU TỪ ẢNH: {image_file} ---\n")
            extracted_texts.append(result.stdout.strip())
            extracted_texts.append(f"\n--- KẾT THÚC ẢNH: {image_file} ---\n")
        else:
            print(f"Lỗi khi xử lý ảnh {image_file} (mã lỗi: {result.returncode}):")
            print(result.stderr)
            extracted_texts.append(f"\n--- LỖI khi xử lý ảnh: {image_file} ---\n")
            extracted_texts.append(result.stderr.strip())

    except FileNotFoundError:
        print(f"Lỗi: Lệnh Tesseract không được tìm thấy. Đảm bảo TESSERACT_PATH là đúng.")
        break
    except Exception as e:
        print(f"Có lỗi xảy ra khi xử lý ảnh {image_file}: {e}")
        extracted_texts.append(f"\n--- NGOẠI LỆ khi xử lý ảnh: {image_file} ---\n")
        extracted_texts.append(str(e))

# --- Lưu tất cả văn bản đã trích xuất vào một file duy nhất ---
with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(extracted_texts))

print(f"Đã hoàn tất trích xuất văn bản từ {len(image_files)} ảnh.")
print(f"Kết quả được lưu vào file: {os.path.abspath(OUTPUT_TEXT_FILE)}")
print("Vui lòng gửi nội dung của file này cho tôi để tiếp tục xử lý thành câu trắc nghiệm Markdown.")