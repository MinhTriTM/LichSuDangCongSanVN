import re

def doc_so_latinh(n):
    n = int(n)
    dv = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    if n < 10: return dv[n]
    if n < 100:
        chuc, dvi = divmod(n, 10)
        s = "mười" if chuc == 1 else dv[chuc] + " mươi"
        if dvi == 1 and chuc > 1: s += " mốt"
        elif dvi == 4 and chuc > 1: s += " tư"
        elif dvi == 5: s += " lăm"
        elif dvi != 0: s += " " + dv[dvi]
        return s
    if n < 1000:
        tram, du = divmod(n, 100)
        s = dv[tram] + " trăm"
        if 0 < du < 10: s += " lẻ " + dv[du]
        elif du >= 10: s += " " + doc_so_latinh(du)
        return s
    if n < 10000:
        nghin, du = divmod(n, 1000)
        s = dv[nghin] + " nghìn"
        if 0 < du < 100: s += " không trăm " + ("lẻ " if du < 10 else "") + doc_so_latinh(du)
        elif du >= 100: s += " " + doc_so_latinh(du)
        return s
    return str(n)

def convert_line(line):
    # 1. Đổi số La Mã (I-XX) - Dùng \b để không dính vào chữ Xương, Việt...
    dict_lama = {'XX':'hai mươi','XIX':'mười chín','XVIII':'mười tám','XVII':'mười bảy','XVI':'mười sáu','XV':'mười lăm','XIV':'mười bốn','XIII':'mười ba','XII':'mười hai','XI':'mười một','X':'mười','IX':'chín','VIII':'tám','VII':'bảy','VI':'sáu','V':'năm','IV':'bốn','III':'ba','II':'hai','I':'một'}
    for k, v in dict_lama.items():
        line = re.sub(r'\b' + k + r'\b', v, line)

    # 2. Đổi tất cả số La Tinh (từ 1 đến 4 chữ số - cân hết năm 1858, 1930...)
    line = re.sub(r'\b\d{1,4}\b', lambda m: doc_so_latinh(m.group()), line)
    
    # 3. Dọn dẹp ký hiệu
    line = line.replace('/', ' tháng ').replace('-', ' đến ')
    return " ".join(line.split())
# --- PHẦN ĐỌC XUẤT FILE ---
try:
    with open('LSD_ko_loi - Copy.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('ket_qua.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(convert_line(line) + '\n')
    print(">>> Đã xử lý xong! File 'ket_qua.txt' đã sẵn sàng.")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file 'data.txt'. Hãy để nó cùng thư mục với script này.")
