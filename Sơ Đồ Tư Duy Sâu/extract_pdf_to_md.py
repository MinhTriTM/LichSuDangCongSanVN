import sys
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Vui lòng cài đặt PyMuPDF: pip install pymupdf")
    sys.exit(1)

def pdf_to_markdown(pdf_path, md_path):
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    md_content = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        # Một số xử lý cơ bản để tạo định dạng Markdown
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Giả định các dòng viết hoa toàn bộ và ngắn là tiêu đề
            if line.isupper() and len(line) < 100:
                md_content.append(f"\n## {line}\n")
            else:
                md_content.append(line)
        
        md_content.append("\n\n--- Page Break ---\n\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    
    print(f"Đã chuyển đổi thành công sang {md_path}")

if __name__ == "__main__":
    pdf_input = r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Lịch Sử Đảng.pdf"
    md_output = r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Lich_Su_Dang_PDF.md"
    pdf_to_markdown(pdf_input, md_output)
