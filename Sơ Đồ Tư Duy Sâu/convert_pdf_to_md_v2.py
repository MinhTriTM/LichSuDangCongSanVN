import fitz  # PyMuPDF
import os
import re

def convert_pdf_to_md(pdf_path, md_path):
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file tại {pdf_path}")
        return

    print(f"Đang đọc file PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    md_content = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        lines = text.split('\n')
        formatted_page = [f"<!-- Page {page_num + 1} -->"]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Nhận diện tiêu đề Chương
            if re.match(r'^Chương\s+\d+', line, re.IGNORECASE):
                formatted_page.append(f"\n# {line}\n")
            # Nhận diện tiêu đề lớn I, II, III...
            elif re.match(r'^[IVX]+\.\s+', line):
                formatted_page.append(f"\n## {line}\n")
            # Nhận diện tiêu đề 1, 2, 3...
            elif re.match(r'^\d+\.\s+', line):
                formatted_page.append(f"\n### {line}\n")
            else:
                formatted_page.append(line)
        
        md_content.append("\n".join(formatted_page))

    print(f"Đang ghi kết quả ra file: {md_path}")
    with open(md_path, "w", encoding="utf-8-sig") as f:
        f.write("\n\n---\n\n".join(md_content))

    print("Hoàn tất chuyển đổi.")

if __name__ == "__main__":
    pdf_input = r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\GiaoTrinh_LSD.pdf"
    md_output = r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\GiaoTrinh_LSD_PDF.md"
    convert_pdf_to_md(pdf_input, md_output)
