import fitz  # PyMuPDF
import os

def convert_pdf_to_md(pdf_path, md_path):
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file tại {pdf_path}")
        return

    print(f"Đang đọc file PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    md_content = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        # Thêm đánh dấu trang trong Markdown
        md_content += f"\n\n<!-- Page {page_num + 1} -->\n\n"
        md_content += text

    print(f"Đang ghi kết quả ra file: {md_path}")
    with open(md_path, "w", encoding="utf-8-sig") as f:
        f.write(md_content)

    print("Hoàn tất chuyển đổi.")

if __name__ == "__main__":
    pdf_input = r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\GiaoTrinh_LSD.pdf"
    md_output = r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\GiaoTrinh_LSD_PDF.md"
    convert_pdf_to_md(pdf_input, md_output)
