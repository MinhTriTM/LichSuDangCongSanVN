# -*- coding: utf-8 -*-
"""
Script phân tích và sửa lỗi file JSON ngân hàng câu hỏi trắc nghiệm Lịch sử Đảng.
Xử lý 6 loại lỗi:
1. Mất chữ đầu / Khuyết đoạn đầu
2. Đáp án bị cắt xén
3. Thiếu số lượng phương án
4. Sai format thứ tự phương án
5. Lỗi OCR (chQ, cQa, phQ)
6. Câu hỏi lặp lại
"""
import json
import re
import os
from collections import Counter

# === CẤU HÌNH ===
INPUT_FILE = r'd:\Download\Thi\LSD\tracnghiem_LSD_chuong_gemini.json'
OUTPUT_FILE = r'd:\Download\Thi\LSD\tracnghiem_LSD_chuong_gemini_fixed.json'
REPORT_FILE = r'd:\Download\Thi\LSD\bao_cao_loi.md'

print("Đang đọc file...")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
total_original = len(questions)
print(f"Tổng số câu hỏi: {total_original}")

report = []
report.append("# BÁO CÁO PHÂN TÍCH & SỬA LỖI\n")
report.append(f"**File gốc:** `{os.path.basename(INPUT_FILE)}`\n")
report.append(f"**Tổng câu hỏi ban đầu:** {total_original}\n\n")

# ============================================================
# LỖI 5: OCR - chQ -> chủ, cQa -> của, phQ -> phủ, PhQ -> Phủ
# ============================================================
print("\n--- LỖI 5: Sửa OCR ---")
report.append("## 1. LỖI OCR (chQ → chủ, cQa → của, phQ → phủ)\n")

ocr_replacements = {
    'chQ': 'chủ',
    'cQa': 'của', 
    'phQ': 'phủ',
    'PhQ': 'Phủ',
}

ocr_fixes = []
for i, q in enumerate(questions):
    for field in ['question', 'answer']:
        original = q[field]
        fixed = original
        for old, new in ocr_replacements.items():
            fixed = fixed.replace(old, new)
        if fixed != original:
            ocr_fixes.append((i, field, original[:80], fixed[:80]))
            q[field] = fixed
    
    new_opts = []
    for j, opt in enumerate(q['options']):
        original = opt
        fixed = opt
        for old, new in ocr_replacements.items():
            fixed = fixed.replace(old, new)
        if fixed != original:
            ocr_fixes.append((i, f'option_{j}', original[:80], fixed[:80]))
        new_opts.append(fixed)
    q['options'] = new_opts

print(f"  Đã sửa {len(ocr_fixes)} lỗi OCR")
report.append(f"- **Đã sửa:** {len(ocr_fixes)} chỗ\n")
if ocr_fixes:
    report.append("- Chi tiết:\n")
    for idx, field, old_text, new_text in ocr_fixes[:20]:
        report.append(f"  - `[{idx}]` {field}: `{old_text}` → `{new_text}`\n")
    if len(ocr_fixes) > 20:
        report.append(f"  - ... và {len(ocr_fixes)-20} chỗ khác\n")
report.append("\n")

# ============================================================
# LỖI 1: Mất chữ đầu / Khuyết đoạn đầu
# ============================================================
print("\n--- LỖI 1: Mất chữ đầu ---")
report.append("## 2. MẤT CHỮ ĐẦU / KHUYẾT ĐOẠN ĐẦU\n")

lower_start_questions = []
digit_start_questions = []
for i, q in enumerate(questions):
    text = q['question'].strip()
    if not text:
        continue
    c = text[0]
    # Chữ cái thường ở đầu câu
    if c.islower() or c in 'àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ':
        lower_start_questions.append((i, text[:120]))
    # Dính số ở đầu
    if c.isdigit():
        rest = text.lstrip('0123456789')
        if rest and rest[0] == ' ':
            digit_start_questions.append((i, text[:120]))

print(f"  Câu bắt đầu chữ thường: {len(lower_start_questions)}")
print(f"  Câu dính số ở đầu: {len(digit_start_questions)}")

report.append(f"### Câu bắt đầu bằng chữ thường: {len(lower_start_questions)}\n")
report.append("> ⚠️ Các câu này cần kiểm tra thủ công để bổ sung chữ/đoạn bị thiếu\n\n")
for idx, txt in lower_start_questions:
    report.append(f"- `[Câu {idx}]` {txt}\n")

report.append(f"\n### Câu dính số ở đầu: {len(digit_start_questions)}\n")
for idx, txt in digit_start_questions:
    report.append(f"- `[Câu {idx}]` {txt}\n")

# Tự động sửa: Xóa số dính ở đầu
for idx, _ in digit_start_questions:
    text = questions[idx]['question'].strip()
    questions[idx]['question'] = re.sub(r'^\d+\s+', '', text)

report.append(f"\n> ✅ Đã tự động xóa số dính ở đầu {len(digit_start_questions)} câu\n\n")

# ============================================================
# LỖI 2: Đáp án bị cắt xén
# ============================================================
print("\n--- LỖI 2: Đáp án bị cắt xén ---")
report.append("## 3. ĐÁP ÁN BỊ CẮT XÉN\n")

cut_words = [' và', ' của', ' tư', ' cho', ' để', ' là', ' về', ' theo', ' trong', 
             ' với', ' đã', ' một', ' các', ' có', ' được', ' do', ' từ', ' lên', 
             ' ra', ' vào', ' mà', ' này', ' đó', ' hay', ' hoặc']
cut_answers = []
for i, q in enumerate(questions):
    for j, opt in enumerate(q['options']):
        opt_clean = opt.strip()
        # Đáp án không kết thúc bằng ký tự hoàn chỉnh
        if opt_clean:
            last_char = opt_clean[-1]
            if last_char not in '.)?!…;:"\'':
                for cw in cut_words:
                    if opt_clean.endswith(cw):
                        cut_answers.append((i, j, chr(65+j), opt_clean, q['question'][:60]))
                        break

print(f"  Đáp án nghi bị cắt xén: {len(cut_answers)}")
report.append(f"- **Tổng nghi bị cắt:** {len(cut_answers)}\n")
report.append("> ⚠️ Cần kiểm tra thủ công, không thể tự đoán nội dung bị thiếu\n\n")
for idx, opt_idx, letter, opt_text, q_text in cut_answers:
    report.append(f"- `[Câu {idx}]` Đáp án **{letter}**: ...{opt_text[-60:]}\n")
    report.append(f"  - Câu hỏi: {q_text}\n")
report.append("\n")

# ============================================================
# LỖI 3: Thiếu phương án (< 4 đáp án)
# ============================================================
print("\n--- LỖI 3: Thiếu phương án ---")
report.append("## 4. THIẾU SỐ LƯỢNG PHƯƠNG ÁN (< 4)\n")

missing_opts = []
for i, q in enumerate(questions):
    n = len(q['options'])
    if n < 4:
        missing_opts.append((i, n, q['question'][:100]))

print(f"  Câu thiếu đáp án: {len(missing_opts)}")
report.append(f"- **Tổng:** {len(missing_opts)} câu\n")
report.append("> ⚠️ Cần bổ sung đáp án thủ công\n\n")
for idx, cnt, txt in missing_opts:
    report.append(f"- `[Câu {idx}]` Chỉ có **{cnt}** đáp án: {txt}\n")
report.append("\n")

# ============================================================
# LỖI 4: Sai format thứ tự phương án
# ============================================================
print("\n--- LỖI 4: Sai format thứ tự ---")
report.append("## 5. SAI FORMAT THỨ TỰ PHƯƠNG ÁN\n")

expected_letters = ['A', 'B', 'C', 'D']
wrong_order = []
for i, q in enumerate(questions):
    opts = q['options']
    letters = []
    for o in opts:
        o_s = o.strip()
        match = re.match(r'^([A-Z])\.\s', o_s)
        if match:
            letters.append(match.group(1))
        else:
            letters.append('?')
    expected = expected_letters[:len(opts)]
    if letters != expected:
        wrong_order.append((i, letters, expected, q['question'][:80]))

print(f"  Câu sai thứ tự: {len(wrong_order)}")
report.append(f"- **Tổng:** {len(wrong_order)} câu\n")
for idx, got, exp, txt in wrong_order:
    report.append(f"- `[Câu {idx}]` Có: {got}, Cần: {exp}\n")
    report.append(f"  - {txt}\n")

# Tự động sửa: đổi lại ký tự đầu cho đúng A, B, C, D
fixed_order = 0
for idx, got, exp, txt in wrong_order:
    opts = questions[idx]['options']
    new_opts = []
    old_answer = questions[idx]['answer']
    for j, opt in enumerate(opts):
        correct_letter = expected_letters[j]
        # Thay thế ký tự đầu
        new_opt = re.sub(r'^[A-Z]\.\s', f'{correct_letter}. ', opt.strip())
        # Nếu đáp án cũ chứa option text cũ, cập nhật
        if opt.strip() == old_answer.strip():
            questions[idx]['answer'] = new_opt
        new_opts.append(new_opt)
    questions[idx]['options'] = new_opts
    fixed_order += 1

report.append(f"\n> ✅ Đã tự động sửa thứ tự {fixed_order} câu\n\n")

# ============================================================
# LỖI 6: Câu hỏi lặp lại
# ============================================================
print("\n--- LỖI 6: Câu hỏi lặp ---")
report.append("## 6. CÂU HỎI BỊ LẶP LẠI\n")

q_texts = [q['question'].strip() for q in questions]
counter = Counter(q_texts)
duplicates = [(text, count) for text, count in counter.items() if count > 1]
duplicates.sort(key=lambda x: -x[1])
total_dup_extra = sum(c - 1 for _, c in duplicates)

print(f"  Nhóm câu lặp: {len(duplicates)}")
print(f"  Bản sao thừa: {total_dup_extra}")
report.append(f"- **Nhóm câu lặp:** {len(duplicates)}\n")
report.append(f"- **Bản sao thừa sẽ xóa:** {total_dup_extra}\n\n")
for text, count in duplicates[:30]:
    report.append(f"- [{count} lần] {text[:100]}\n")
if len(duplicates) > 30:
    report.append(f"- ... và {len(duplicates)-30} nhóm khác\n")

# Loại bỏ trùng lặp (giữ bản đầu tiên)
seen = set()
unique_questions = []
removed = 0
for q in questions:
    q_text = q['question'].strip()
    if q_text not in seen:
        seen.add(q_text)
        unique_questions.append(q)
    else:
        removed += 1

print(f"  Đã loại: {removed} câu trùng")
report.append(f"\n> ✅ Đã loại bỏ **{removed}** câu trùng lặp\n\n")

# ============================================================
# CẬP NHẬT VÀ GHI FILE
# ============================================================
data['questions'] = unique_questions
data['totalQ'] = len(unique_questions)

# Cập nhật section counts
section_counts = Counter(q['section'] for q in unique_questions)
for sec in data['sections']:
    sec['count'] = section_counts.get(sec['key'], 0)

report.append("---\n\n## TỔNG KẾT\n\n")
report.append(f"| Hạng mục | Số lượng |\n")
report.append(f"|----------|----------|\n")
report.append(f"| Câu hỏi ban đầu | **{total_original}** |\n")
report.append(f"| Câu sau khi loại trùng | **{len(unique_questions)}** |\n")
report.append(f"| Đã loại câu trùng | **{removed}** |\n")
report.append(f"| Sửa OCR | **{len(ocr_fixes)}** |\n")
report.append(f"| Sửa thứ tự đáp án | **{fixed_order}** |\n")
report.append(f"| Xóa số dính đầu | **{len(digit_start_questions)}** |\n\n")

report.append("### Phân bố theo chương:\n\n")
for sec in data['sections']:
    report.append(f"- **{sec['label']}**: {sec['count']} câu\n")

report.append("\n### Lỗi cần sửa thủ công:\n\n")
report.append(f"- Câu bắt đầu chữ thường (mất chữ đầu): **{len(lower_start_questions)}**\n")
report.append(f"- Đáp án nghi bị cắt xén: **{len(cut_answers)}**\n")
report.append(f"- Câu thiếu phương án: **{len(missing_opts)}**\n")

# Ghi file JSON đã sửa
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nĐã ghi file đã sửa: {OUTPUT_FILE}")

# Ghi báo cáo
with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(report)
print(f"Đã ghi báo cáo: {REPORT_FILE}")

print(f"\n=== KẾT QUẢ ===")
print(f"Câu hỏi: {total_original} → {len(unique_questions)} (loại {removed} trùng)")
print(f"Sửa OCR: {len(ocr_fixes)}")
print(f"Sửa thứ tự: {fixed_order}")
print(f"Cần sửa thủ công: mất chữ đầu={len(lower_start_questions)}, cắt xén={len(cut_answers)}, thiếu đáp án={len(missing_opts)}")
