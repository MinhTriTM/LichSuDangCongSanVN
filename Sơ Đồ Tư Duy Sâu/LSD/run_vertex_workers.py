import urllib.request
import json
import subprocess
import concurrent.futures
import time
import os

PROJECT_ID = "tool-dich-thuat"
LOCATION = "global"
MODEL_ID = "gemini-3.1-pro-preview"

print("Đang lấy Access Token từ gcloud...")
try:
    ACCESS_TOKEN = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
except Exception as e:
    print(f"[-] LỖI: Không thể lấy access token. {e}")
    print("Vui lòng đảm bảo bạn đã cài đặt Google Cloud CLI và đã chạy lệnh 'gcloud auth login'.")
    exit(1)

URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:generateContent"

WORKERS = [
    {
        "file": "phan1_1858_1930.json",
        "prompt": "Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Dựa trên toàn bộ dữ liệu lịch sử từ 1858 đến tháng 2/1930, hãy tạo một CSDL dạng JSON cấu trúc cây (Hierarchy) siêu chi tiết gồm 8 tầng (Thế kỷ -> Giai đoạn -> Năm -> Tháng -> Sự kiện -> Chi tiết -> Ý nghĩa -> Bài học). Bắt buộc bóc tách 100% các dữ liệu sau: 1. Sự kiện Pháp nổ súng tại Đà Nẵng, Gia Định và chi tiết các điều khoản của 4 Hiệp ước. 2. Các chính sách cai trị và sự phân hóa 5 giai cấp. 3. Phong trào Cần Vương, Yên Thế, Đông Du, Duy Tân, Yên Bái. 4. Quá trình ra đời 3 tổ chức Cộng sản (1929). 5. Hội nghị hợp nhất Đảng (6/1 - 7/2/1930) và nội dung chi tiết Cương lĩnh chính trị đầu tiên. Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, bắt đầu bằng { và kết thúc bằng }, không bọc trong markdown. Tại mỗi Node lá (cuối cùng), trường 'details' phải chứa từ 150-300 từ phân tích chuyên sâu."
    },
    {
        "file": "phan2_1930_1945.json",
        "prompt": "Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng cho giai đoạn 1930 - 1945. Bắt buộc bóc tách 100% các dữ liệu sau: 1. Cao trào 1930-1931 và Xô Viết Nghệ Tĩnh. 2. HNTW 1 (10/1930): Nội dung Luận cương Trần Phú, phân tích cặn kẽ khuyết điểm 'Tả khuynh'. 3. Cao trào dân chủ 1936-1939. 4. Chuyển hướng chiến lược đặt GPDT lên hàng đầu qua các HNTW 6, 7, 8 (Pác Bó). 5. Mặt trận Việt Minh. 6. Cách mạng Tháng 8 (1945): Nhật Pháp bắn nhau, chớp Thời cơ vàng, Hội nghị Tân Trào, Tuyên ngôn Độc lập, Tính chất và 4 Bài học. Yêu cầu: Trả về JSON thuần (không markdown), node lá chứa 150-300 chữ."
    },
    {
        "file": "phan3_1945_1954.json",
        "prompt": "Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Tạo CSDL JSON cây 8 tầng cho 1945 - 1954. Bắt buộc: 1. Tình thế Ngàn cân treo sợi tóc. 2. Sách lược ngoại giao: Hiệp định Sơ bộ (6/3) và Tạm ước (14/9). 3. Lời kêu gọi Toàn quốc kháng chiến (19/12/1946) và đường lối kháng chiến. 4. Chiến dịch: Việt Bắc (1947), Biên Giới (1950). 5. Đại hội II (2/1951). 6. Đỉnh cao Điện Biên Phủ (1954): Kế hoạch Nava, 56 ngày đêm, Hiệp định Geneva và Bài học kinh nghiệm. Yêu cầu: JSON thuần, node lá chứa 150-300 chữ."
    },
    {
        "file": "phan4_1954_1975.json",
        "prompt": "Đóng vai trò là Giáo sư Lịch sử Đảng. Tạo CSDL JSON cây 8 tầng cho 1954 - 1975. Bắt buộc: 1. Đại hội III (1960). 2. Đánh bại Chiến tranh Đơn phương (1954-1960) & Đồng Khởi. 3. Đánh bại Chiến tranh Đặc biệt (1961-1965). 4. Đánh bại Chiến tranh Cục bộ (1965-1968) & Mậu Thân 1968. 5. Đánh bại VN Hóa chiến tranh (1969-1973) & ĐBP trên không. 6. Đại thắng Mùa Xuân 1975: Chiến dịch Tây Nguyên, Huế - Đà Nẵng, Hồ Chí Minh. Tính chất, ý nghĩa, và 4 bài học. Yêu cầu: JSON thuần, node lá chứa 150-300 chữ."
    },
    {
        "file": "phan5_1975_1996.json",
        "prompt": "Đóng vai trò là Giáo sư Lịch sử Đảng. Tạo CSDL JSON cây 8 tầng cho 1975 - 1996. Bắt buộc: 1. Đại hội IV (1976), ĐH V (1982): Phân tích nguyên nhân khủng hoảng kinh tế. 2. Ba bước đột phá tiền Đổi mới: HNTW 6 (1979), Chỉ thị 100, Giá-Lương-Tiền. 3. Đại hội VI (1986): Đổi Mới toàn diện, chuyển sang KT hàng hóa, 3 chương trình KT lớn. 4. Đại hội VII (1991): Cương lĩnh 1991. 5. Đại hội VIII (1996). Yêu cầu: JSON thuần, node lá chứa 150-300 chữ phân tích chuyên sâu."
    },
    {
        "file": "phan6_1996_2026.json",
        "prompt": "Đóng vai trò là Giáo sư Lịch sử Đảng. Tạo CSDL JSON cây 8 tầng cho 1996 - 2026. Bắt buộc: 1. Đại hội IX (2001). 2. Đại hội X (2006). 3. Đại hội XI (2011), XII (2016): Phòng chống tham nhũng (Đốt lò), KT tư nhân. 4. Đại hội XIII (2021): Tầm nhìn 2025, 2030, 2045. Ngoại giao Cây tre. 5. Đại hội XIV (2026): Kỷ nguyên vươn mình, Tinh - Gọn - Mạnh. Yêu cầu: JSON thuần, node lá chứa 150-300 chữ."
    },
    {
        "file": "phan7_hochiminh.json",
        "prompt": "Đóng vai trò là chuyên gia Tư tưởng Hồ Chí Minh. Tạo CSDL JSON cây 8 tầng Hành trình Bác Hồ (1890 - 1969). Bắt buộc: 1. Bến Nhà Rồng (1911), Yêu sách 8 điểm (1919), Đọc Luận cương Lênin (1920). 2. Các tác phẩm kinh điển. 3. Tư duy ngoại giao Dĩ bất biến ứng vạn biến. 4. Quyết sách chỉ đạo các chiến dịch. 5. Bản Di chúc thiêng liêng (1969). Yêu cầu: JSON thuần, không bọc markdown."
    },
    {
        "file": "phan8_quocte.json",
        "prompt": "Đóng vai trò chuyên gia Quan hệ Quốc tế. Tạo CSDL JSON cây 8 tầng về Bối cảnh thế giới tác động đến Đảng. Bắt buộc: 1. CM Tháng 10 Nga & Quốc tế III. 2. Cục diện Thế chiến 2 & Thời cơ vàng. 3. Chiến tranh Lạnh và mâu thuẫn Xô-Trung. 4. Sự sụp đổ của Liên Xô. 5. Giai đoạn Hội nhập và Ngoại giao Cây tre. Yêu cầu: JSON thuần, không bọc markdown."
    },
    {
        "file": "phan9_tracnghiem.json",
        "prompt": "Hãy tạo một JSON giả lập bộ 50 câu trắc nghiệm Lịch sử Đảng (do payload quá lớn không truyền trực tiếp file 1131 câu vào prompt được). Quy tắc: Root là 'TỔNG ÔN TRẮC NGHIỆM', Tầng 1 là Các Chương, Tầng 2 là 'Nhóm 20 câu', Tầng 3 là Cấu trúc { name: 'câu hỏi ngắn', question, options: [], answer, details: 'giải thích sâu' }. Tuyệt đối chỉ trả về JSON thuần."
    }
]

def call_vertex_ai(worker):
    filename = worker['file']
    prompt = worker['prompt']
    
    print(f"[*] Worker [{filename}] đang gửi request lên Vertex AI...")
    
    data = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 8192
        }
    }
    
    req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'))
    req.add_header('Authorization', f'Bearer {ACCESS_TOKEN}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            try:
                content_text = result['candidates'][0]['content']['parts'][0]['text']
                
                # Làm sạch markdown nếu Model cố tình nhét vào
                content_text = content_text.strip()
                if content_text.startswith("```json"):
                    content_text = content_text[7:]
                if content_text.startswith("```"):
                    content_text = content_text[3:]
                if content_text.endswith("```"):
                    content_text = content_text[:-3]
                
                content_text = content_text.strip()
                
                # Đảm bảo thư mục data tồn tại
                os.makedirs("data", exist_ok=True)
                
                with open(f"data/{filename}", 'w', encoding='utf-8') as f:
                    f.write(content_text)
                    
                print(f"[+] THÀNH CÔNG: Đã lưu {filename}")
            except KeyError:
                print(f"[-] LỖI API: Response không hợp lệ tại {filename}")
    except Exception as e:
        print(f"[-] LỖI KẾT NỐI tại {filename}: {e}")

def main():
    print(f"\nBẮT ĐẦU CHẠY 9 WORKERS SONG SONG BẰNG THREAD POOL EXECUTOR...")
    print(f"Model: {MODEL_ID} | Vùng: {LOCATION}\n")
    start_time = time.time()
    
    # Số luồng (thread) chạy song song = 9
    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
        executor.map(call_vertex_ai, WORKERS)
        
    print(f"\n=> HOÀN TẤT TẤT CẢ! Thời gian chạy: {time.time() - start_time:.2f} giây.")

if __name__ == "__main__":
    main()
