// Script Node.js sửa lỗi file JSON ngân hàng câu hỏi trắc nghiệm LSD
// Chạy: node fix_json.js

const fs = require('fs');
const path = require('path');

const INPUT = path.join(__dirname, 'tracnghiem_LSD_chuong_gemini.json');
const OUTPUT = path.join(__dirname, 'tracnghiem_LSD_chuong_gemini_fixed.json');
const REPORT = path.join(__dirname, 'bao_cao_loi.md');

console.log('Đang đọc file...');
const raw = fs.readFileSync(INPUT, 'utf-8');
const data = JSON.parse(raw);
let questions = data.questions;
console.log(`Tổng câu hỏi: ${questions.length}`);

const report = [];
report.push('# BÁO CÁO PHÂN TÍCH & SỬA LỖI\n\n');
report.push(`**Tổng câu gốc:** ${questions.length}\n\n`);

// ============================================================
// LỖI 5: OCR - chQ -> chủ, cQa -> của, phQ -> phủ
// ============================================================
const ocrMap = [['chQ','chủ'],['cQa','của'],['phQ','phủ'],['PhQ','Phủ']];
let ocrFixes = 0;
questions.forEach((q, i) => {
  ocrMap.forEach(([old, nw]) => {
    if (q.question.includes(old)) { q.question = q.question.replaceAll(old, nw); ocrFixes++; }
    if (q.answer.includes(old)) { q.answer = q.answer.replaceAll(old, nw); ocrFixes++; }
    q.options = q.options.map(o => {
      if (o.includes(old)) { ocrFixes++; return o.replaceAll(old, nw); }
      return o;
    });
  });
});
console.log(`Sửa OCR: ${ocrFixes}`);
report.push(`## LỖI 5: OCR\n- Đã sửa: **${ocrFixes}** chỗ\n\n`);

// ============================================================
// LỖI 1b: Xóa số dính ở đầu câu
// ============================================================
let digitFixes = 0;
const digitFixDetails = [];
questions.forEach((q, i) => {
  const text = q.question.trim();
  if (/^\d+\s+[A-ZĐ]/.test(text)) {
    const oldText = text.substring(0, 80);
    q.question = text.replace(/^\d+\s+/, '');
    digitFixes++;
    digitFixDetails.push(`  - [${i}] "${oldText}" → "${q.question.substring(0, 80)}"`);
  }
});
console.log(`Xóa số dính: ${digitFixes}`);
report.push(`## LỖI 1b: Số dính ở đầu\n- Đã sửa: **${digitFixes}** câu\n`);
digitFixDetails.forEach(d => report.push(d + '\n'));
report.push('\n');

// ============================================================
// LỖI 4: Sửa thứ tự đáp án A,B,C,D
// ============================================================
const expectedLetters = ['A','B','C','D'];
let orderFixes = 0;
const orderFixDetails = [];
questions.forEach((q, i) => {
  const opts = q.options;
  const letters = opts.map(o => { const m = o.trim().match(/^([A-Z])\./); return m ? m[1] : '?'; });
  const exp = expectedLetters.slice(0, opts.length);
  if (JSON.stringify(letters) !== JSON.stringify(exp)) {
    orderFixDetails.push(`  - [${i}] ${letters.join(',')} → ${exp.join(',')}: ${q.question.substring(0, 60)}`);
    opts.forEach((opt, j) => {
      const cl = expectedLetters[j];
      const newOpt = opt.trim().replace(/^[A-Z]\.\s/, cl + '. ');
      if (opt.trim() === q.answer.trim()) q.answer = newOpt;
      q.options[j] = newOpt;
    });
    orderFixes++;
  }
});
console.log(`Sửa thứ tự: ${orderFixes}`);
report.push(`## LỖI 4: Sai thứ tự phương án\n- Đã sửa: **${orderFixes}** câu\n`);
orderFixDetails.forEach(d => report.push(d + '\n'));
report.push('\n');

// ============================================================
// LỖI 6: Loại bỏ câu trùng lặp
// ============================================================
// Đếm trước
const countMap = {};
questions.forEach(q => {
  const t = q.question.trim();
  countMap[t] = (countMap[t] || 0) + 1;
});
const dupeGroups = Object.entries(countMap).filter(([_, c]) => c > 1).sort((a, b) => b[1] - a[1]);

const seen = new Set();
const uniqueQ = [];
let removed = 0;
questions.forEach(q => {
  const t = q.question.trim();
  if (!seen.has(t)) { seen.add(t); uniqueQ.push(q); } else { removed++; }
});
console.log(`Loại trùng: ${removed} (${dupeGroups.length} nhóm)`);

report.push(`## LỖI 6: Câu hỏi lặp lại\n`);
report.push(`- Nhóm lặp: **${dupeGroups.length}**\n`);
report.push(`- Bản sao đã xóa: **${removed}**\n`);
report.push(`- Top câu lặp nhiều nhất:\n`);
dupeGroups.slice(0, 30).forEach(([text, count]) => {
  report.push(`  - [${count} lần] ${text.substring(0, 100)}\n`);
});
report.push('\n');

// Cập nhật data
data.questions = uniqueQ;
data.totalQ = uniqueQ.length;
const sc = {};
uniqueQ.forEach(q => { sc[q.section] = (sc[q.section] || 0) + 1; });
data.sections.forEach(s => { s.count = sc[s.key] || 0; });

// ============================================================
// THỐNG KÊ LỖI CÒN LẠI (cần sửa thủ công)
// ============================================================

// Lỗi 1: Câu bắt đầu chữ thường
const lowerStart = [];
uniqueQ.forEach((q, i) => {
  const text = q.question.trim();
  if (text && /^[a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]/.test(text)) {
    lowerStart.push({idx: i, text: text.substring(0, 150)});
  }
});
report.push(`## LỖI 1: Mất chữ đầu (CẦN SỬA THỦ CÔNG)\n`);
report.push(`- Tổng: **${lowerStart.length}** câu\n`);
report.push(`> ⚠️ Không thể tự đoán chữ/đoạn bị thiếu\n\n`);
lowerStart.forEach(({idx, text}) => {
  report.push(`- \`[Câu ${idx}]\` ${text}\n`);
});
report.push('\n');

// Lỗi 3: Thiếu đáp án
const missingOpts = [];
uniqueQ.forEach((q, i) => {
  if (q.options.length < 4) {
    missingOpts.push({idx: i, count: q.options.length, text: q.question.substring(0, 100)});
  }
});
report.push(`## LỖI 3: Thiếu phương án (CẦN SỬA THỦ CÔNG)\n`);
report.push(`- Tổng: **${missingOpts.length}** câu\n`);
report.push(`> ⚠️ Cần bổ sung đáp án từ nguồn gốc\n\n`);
missingOpts.forEach(({idx, count, text}) => {
  report.push(`- \`[Câu ${idx}]\` Chỉ có **${count}** đáp án: ${text}\n`);
});
report.push('\n');

// Lỗi 2: Đáp án bị cắt
const cutWords = [' và',' của',' tư',' cho',' để',' là',' về',' theo',' trong',' với',' đã',' một',' các',' có',' được',' do',' từ',' lên',' ra',' vào',' mà'];
const cutAnswers = [];
uniqueQ.forEach((q, i) => {
  q.options.forEach((opt, j) => {
    const clean = opt.trim();
    const last = clean[clean.length - 1];
    if (last && !'.)?!…;:"\''.includes(last)) {
      for (const cw of cutWords) {
        if (clean.endsWith(cw)) {
          cutAnswers.push({idx: i, letter: String.fromCharCode(65+j), ending: clean.slice(-70), qText: q.question.substring(0, 80)});
          break;
        }
      }
    }
  });
});
report.push(`## LỖI 2: Đáp án bị cắt xén (CẦN SỬA THỦ CÔNG)\n`);
report.push(`- Tổng: **${cutAnswers.length}** đáp án\n`);
report.push(`> ⚠️ Cần bổ sung phần bị cắt từ nguồn gốc\n\n`);
cutAnswers.forEach(({idx, letter, ending, qText}) => {
  report.push(`- \`[Câu ${idx}]\` Đáp án **${letter}**: ...${ending}\n`);
  report.push(`  - Câu hỏi: ${qText}\n`);
});
report.push('\n');

// ============================================================
// TỔNG KẾT
// ============================================================
report.push('---\n\n## TỔNG KẾT\n\n');
report.push('| Hạng mục | Số lượng |\n');
report.push('|----------|----------|\n');
report.push(`| Câu gốc | **${questions.length}** |\n`);
report.push(`| Sau khi sửa & loại trùng | **${uniqueQ.length}** |\n`);
report.push(`| Đã loại câu trùng | **${removed}** |\n`);
report.push(`| Sửa OCR | **${ocrFixes}** |\n`);
report.push(`| Xóa số dính đầu | **${digitFixes}** |\n`);
report.push(`| Sửa thứ tự đáp án | **${orderFixes}** |\n\n`);

report.push('### Phân bố theo chương:\n');
data.sections.forEach(s => {
  report.push(`- **${s.label}**: ${s.count} câu\n`);
});
report.push('\n### Lỗi cần sửa thủ công:\n');
report.push(`- Mất chữ đầu: **${lowerStart.length}** câu\n`);
report.push(`- Thiếu đáp án: **${missingOpts.length}** câu\n`);
report.push(`- Đáp án bị cắt: **${cutAnswers.length}** đáp án\n`);

// ============================================================
// GHI FILE
// ============================================================
fs.writeFileSync(OUTPUT, JSON.stringify(data, null, 2), 'utf-8');
console.log(`\nĐã ghi: ${OUTPUT}`);

fs.writeFileSync(REPORT, report.join(''), 'utf-8');
console.log(`Đã ghi: ${REPORT}`);

console.log(`\n=== KẾT QUẢ ===`);
console.log(`${questions.length} → ${uniqueQ.length} câu (loại ${removed} trùng)`);
console.log(`OCR: ${ocrFixes} | Số dính: ${digitFixes} | Thứ tự: ${orderFixes}`);
console.log(`Cần sửa thủ công: chữ thường=${lowerStart.length}, thiếu ĐA=${missingOpts.length}, cắt xén=${cutAnswers.length}`);
