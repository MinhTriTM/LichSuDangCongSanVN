import os
import subprocess

def find_tesseract():
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\tools\Tesseract-OCR\tesseract.exe",
        "tesseract"
    ]
    for path in common_paths:
        try:
            subprocess.run([path, "--version"], capture_output=True)
            return path
        except:
            continue
    return None

tesseract_path = find_tesseract()
image_dir = r"D:\Download\Thi\LSD\BÀI TRẮC NGHIỆM LSĐ"
output_file = r"D:\Download\Thi\LSD\IMGtotexxt.txt"

if not tesseract_path:
    print("OCR_ENGINE_NOT_FOUND")
    exit(1)

image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
success_count = 0
fail_count = 0

with open(output_file, "w", encoding="utf-8") as out:
    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        try:
            result = subprocess.run([tesseract_path, img_path, "stdout", "-l", "vie"], capture_output=True, text=True, encoding="utf-8")
            if result.returncode == 0:
                out.write(f"\n--- {img_file} ---\n")
                out.write(result.stdout)
                success_count += 1
            else:
                out.write(f"\n--- {img_file} (FAIL) ---\n")
                fail_count += 1
        except Exception as e:
            out.write(f"\n--- {img_file} (ERROR: {str(e)}) ---\n")
            fail_count += 1

print(f"SUCCESS:{success_count}")
print(f"FAIL:{fail_count}")
