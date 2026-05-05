# KẾ HOẠCH TRIỂN KHAI ĐA LUỒNG BẰNG VERTEX AI (GEMINI 3.1 PRO PREVIEW)
**Mục tiêu tối thượng:** Xây dựng Đề cương tổng thể Bách Khoa Toàn Thư môn Lịch sử Đảng Cộng sản Việt Nam (Hệ Chuyên - HVCTQG), giúp ghi nhớ toàn bộ kiến thức một cách logic tuyệt đối trong vòng 48 giờ.
**Công nghệ sử dụng:** Vertex AI, Google Cloud CLI, Mô hình `gemini-3.1-pro-preview`.
**Project ID:** `tool-dich-thuat` | **Location:** `global`

---

## I. MÔ HÌNH VÀ KIẾN TRÚC DỮ LIỆU (JSON SCHEMA)
TẤT CẢ các AI phải trả về dữ liệu tuân thủ nghiêm ngặt cấu trúc JSON cây (Hierarchy) của D3.js. Không được chứa ```json hoặc markdown.
```json
{
  "name": "Tên Nhánh (Ví dụ: Đại hội VI - 1986)",
  "details": "Mô tả ngắn gọn bối cảnh, diễn biến chính",
  "children": [
    {
      "name": "Tên Sự kiện cấp 1",
      "details": "Nội dung chi tiết, nguyên nhân, hệ quả, ý nghĩa lịch sử, bài học kinh nghiệm.",
      "children": [] 
    }
  ]
}
```

---

## II. PHÂN CÔNG TÁC VỤ ĐA LUỒNG VÀ PROMPT CHI TIẾT (9 WORKERS)

Hãy copy nội dung trong khối blockquote (`> ...`) dán vào trường `"text"` của Google Cloud CLI.

### 📝 Worker 1: Khởi nguồn & Thành lập Đảng (File: `phan1_1858_1930.json`)
> Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Dựa trên toàn bộ dữ liệu lịch sử từ 1858 đến tháng 2/1930, hãy tạo một CSDL dạng JSON cấu trúc cây (Hierarchy) siêu chi tiết gồm 8 tầng (Thế kỷ -> Giai đoạn -> Năm -> Tháng -> Sự kiện -> Chi tiết -> Ý nghĩa -> Bài học).
> Bắt buộc bóc tách 100% các dữ liệu sau:
> 1. Sự kiện Pháp nổ súng tại Đà Nẵng, Gia Định và chi tiết các điều khoản của 4 Hiệp ước (Nhâm Tuất, Giáp Tuất, Quý Mùi/Harmand, Giáp Thân/Patenôtre). Phân tích sự nhu nhược của triều Nguyễn.
> 2. Các chính sách cai trị (khai thác thuộc địa lần 1 & 2, chia để trị, ngu dân) và sự phân hóa 5 giai cấp, 2 mâu thuẫn cơ bản.
> 3. Phong trào Cần Vương, Yên Thế, Đông Du, Duy Tân, Yên Bái: Nêu rõ phương hướng, người lãnh đạo, diễn biến và bài học kinh nghiệm từ sự thất bại.
> 4. Quá trình ra đời 3 tổ chức Cộng sản (1929).
> 5. Hội nghị hợp nhất Đảng (6/1 - 7/2/1930) và nội dung chi tiết Cương lĩnh chính trị đầu tiên (Chánh cương, Sách lược vắn tắt).
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, bắt đầu bằng { và kết thúc bằng }, không bọc trong ```json. Tại mỗi Node lá (cuối cùng), trường "details" phải chứa từ 150-300 từ phân tích chuyên sâu.

### 📝 Worker 2: Giành Chính quyền (File: `phan2_1930_1945.json`)
> Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng cho giai đoạn 1930 - 1945. 
> Bắt buộc bóc tách 100% các dữ liệu sau:
> 1. Cao trào 1930-1931 và Xô Viết Nghệ Tĩnh (Tính chất, ý nghĩa, bài học).
> 2. HNTW 1 (10/1930): Nội dung Luận cương Trần Phú, phân tích cặn kẽ khuyết điểm "Tả khuynh".
> 3. Cao trào dân chủ 1936-1939: Bối cảnh thế giới, chuyển hướng tại HNTW 7/1936, hình thức đấu tranh và ý nghĩa tập dượt lần 2.
> 4. Chuyển hướng chiến lược đặt GPDT lên hàng đầu qua các HNTW 6 (11/1939), HNTW 7 (11/1940), và HNTW 8 (5/1941) do Bác Hồ chủ trì tại Pác Bó.
> 5. Sự thành lập Mặt trận Việt Minh.
> 6. Cách mạng Tháng 8 (1945): Phân tích Chỉ thị "Nhật Pháp bắn nhau", chớp Thời cơ vàng, Hội nghị Tân Trào, Khởi nghĩa ở 3 thành phố lớn, Tuyên ngôn Độc lập, Tính chất và 4 Bài học kinh nghiệm.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, bắt đầu bằng { và kết thúc bằng }, không bọc trong markdown. Trường "details" ở các node cuối phải phân tích cực kỳ sâu sắc (150-300 chữ).

### 📝 Worker 3: Kháng chiến chống Pháp (File: `phan3_1945_1954.json`)
> Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng cho giai đoạn 1945 - 1954. 
> Bắt buộc bóc tách 100% các dữ liệu sau:
> 1. Tình thế "Ngàn cân treo sợi tóc" (1945-1946): Diệt giặc đói, giặc dốt, giặc ngoại xâm.
> 2. Sách lược ngoại giao "Dĩ bất biến ứng vạn biến": Chi tiết Hiệp định Sơ bộ (6/3) và Tạm ước (14/9).
> 3. Lời kêu gọi Toàn quốc kháng chiến (19/12/1946) và đường lối kháng chiến (Toàn dân, toàn diện, lâu dài, dựa vào sức mình).
> 4. Phân tích các chiến dịch: Việt Bắc (1947), Biên Giới (1950) làm thay đổi cục diện.
> 5. Đại hội II (2/1951): Đổi tên Đảng LĐVN, Chính cương mới, Cải cách ruộng đất (thành tựu và sai lầm Tả khuynh).
> 6. Đỉnh cao Điện Biên Phủ (1954): Kế hoạch Nava, diễn biến 56 ngày đêm, Hiệp định Geneva và Bài học kinh nghiệm chống Pháp.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, không bọc markdown. Trường "details" ở node lá phải chứa 150-300 từ.

### 📝 Worker 4: Kháng chiến chống Mỹ (File: `phan4_1954_1975.json`)
> Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng cho giai đoạn 1954 - 1975. 
> Bắt buộc bóc tách 100% các dữ liệu sau:
> 1. Đại hội III (1960): Đường lối tiến hành đồng thời 2 chiến lược ở 2 miền Nam - Bắc.
> 2. Chiến tranh Đơn phương (1954-1960): Luật 10/59, NQ 15 (1/1959), Phong trào Đồng Khởi.
> 3. Đánh bại Chiến tranh Đặc biệt (1961-1965): Phá ấp chiến lược, chiến thuật trực thăng vận, 3 vùng chiến lược, 3 mũi giáp công, Ấp Bắc, Bình Giã.
> 4. Đánh bại Chiến tranh Cục bộ (1965-1968): NQTW 11 & 12, Mậu Thân 1968 buộc Mỹ ngồi đàm phán Paris.
> 5. Đánh bại VN Hóa chiến tranh (1969-1973): ĐBP trên không (1972), Hiệp định Paris (1973).
> 6. Đại thắng Mùa Xuân 1975: NQTW 21, Chiến dịch Tây Nguyên, Huế - Đà Nẵng, Hồ Chí Minh. Tính chất, ý nghĩa, và 4 bài học kinh nghiệm.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, không bọc markdown. Trường "details" ở node lá phải chứa 150-300 từ.

### 📝 Worker 5: Quá độ và Khởi xướng Đổi Mới (File: `phan5_1975_1996.json`)
> Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng cho giai đoạn 1975 - 1996. 
> Bắt buộc bóc tách 100% các dữ liệu sau:
> 1. Đại hội IV (1976), ĐH V (1982): Phân tích sâu nguyên nhân dẫn đến khủng hoảng kinh tế (duy ý chí, bao cấp, ưu tiên công nghiệp nặng quá mức).
> 2. Ba bước đột phá tiền Đổi mới: HNTW 6 (1979 - Sản xuất bung ra), Chỉ thị 100 (1981 - Khoán chui), Giá-Lương-Tiền (1985).
> 3. Đại hội VI (1986): Đổi Mới toàn diện, chuyển sang KT hàng hóa nhiều thành phần, 3 chương trình KT lớn, 4 bài học cốt lõi (Lấy dân làm gốc...).
> 4. Đại hội VII (1991): Phân tích Cương lĩnh 1991 (Kiên định CNXH giữa lúc Liên Xô sụp đổ), Bình thường hóa với TQ.
> 5. Đại hội VIII (1996): Tuyên bố ra khỏi khủng hoảng, bước vào CNH-HĐH.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, không bọc markdown. Trường "details" ở node lá phải phân tích chuyên sâu.

### 📝 Worker 6: Đẩy mạnh CNH-HĐH & Hội nhập (File: `phan6_1996_2026.json`)
> Đóng vai trò là Giáo sư Lịch sử Đảng tại Học viện Chính trị Quốc gia. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng cho giai đoạn 1996 - 2026. 
> Bắt buộc bóc tách 100% các dữ liệu sau:
> 1. Đại hội IX (2001): Khái niệm Nền kinh tế thị trường định hướng XHCN.
> 2. Đại hội X (2006): Chấp nhận Đảng viên làm kinh tế tư nhân, Gia nhập WTO.
> 3. Đại hội XI (2011), XII (2016): Bổ sung Cương lĩnh, chiến dịch phòng chống tham nhũng (Đốt lò), KT tư nhân là động lực.
> 4. Đại hội XIII (2021): Tầm nhìn chiến lược 2025, 2030, 2045. Đột phá thể chế, hạ tầng, nhân lực. Ngoại giao Cây tre.
> 5. Đại hội XIV (2026 - Dự kiến): Tinh thần Kỷ nguyên vươn mình, Tinh - Gọn - Mạnh.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, không bọc markdown. Trường "details" ở node lá phải phân tích chuyên sâu.

### 📝 Worker 7: Hành trình Bác Hồ (File: `phan7_hochiminh.json`)
> Đóng vai trò là chuyên gia Tư tưởng Hồ Chí Minh. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng mô tả Hành trình của Bác Hồ từ 1890 - 1969. 
> Bắt buộc bóc tách:
> 1. Sự kiện Bến Nhà Rồng (1911), Yêu sách 8 điểm (1919), Đọc Luận cương Lênin (1920) - Phân tích bước ngoặt tư tưởng.
> 2. Các tác phẩm kinh điển: Báo Le Paria, Bản án chế độ thực dân Pháp, Đường Kách mệnh, Ngục trung nhật ký (Hoàn cảnh sáng tác, giá trị lý luận).
> 3. Tư duy ngoại giao "Dĩ bất biến ứng vạn biến" (1946).
> 4. Quyết sách chỉ đạo các chiến dịch Điện Biên Phủ, Đồng Khởi.
> 5. Bản Di chúc thiêng liêng (1969) và giá trị để lại.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, không bọc markdown.

### 📝 Worker 8: Bối cảnh Quốc tế & Ngoại giao (File: `phan8_quocte.json`)
> Đóng vai trò là Chuyên gia Quan hệ Quốc tế. Hãy tạo một CSDL dạng JSON cấu trúc cây 8 tầng phân tích Tác động của Bối cảnh thế giới đến Lịch sử Đảng. 
> Bắt buộc bóc tách:
> 1. Tác động của Cách mạng Tháng 10 Nga & Quốc tế III.
> 2. Cục diện Chiến tranh thế giới 2 tạo Thời cơ vàng cho CMT8.
> 3. Chiến tranh Lạnh và mâu thuẫn Xô-Trung: Cách Đảng CSVN giữ vững đường lối độc lập, tự chủ.
> 4. Khủng hoảng, sụp đổ của Liên Xô: Tác động buộc VN phải Đổi Mới.
> 5. Giai đoạn Hội nhập: Bình thường hóa (TQ, Mỹ), ASEAN, WTO, và phân tích sâu trường phái Ngoại giao Cây tre VN.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, không bọc markdown.

### 📝 Worker 9: Tổng ôn Trắc nghiệm (File: `phan9_tracnghiem.json`)
> Bạn là Hệ thống biến đổi dữ liệu. Dữ liệu đầu vào của bạn là bộ 1131 câu hỏi trắc nghiệm Lịch sử Đảng. Hãy cấu trúc chúng thành một file JSON phân cấp.
> Quy tắc:
> - Root Node: "TỔNG ÔN TRẮC NGHIỆM"
> - Tầng 1: Các Chương (Chương 1 đến Chương 7).
> - Tầng 2: Chia thành các "Nhóm 20 câu" (Ví dụ: Nhóm 1-20, Nhóm 21-40) để tránh nghẽn UI.
> - Tầng 3: Từng câu hỏi. Cấu trúc bắt buộc: { "name": "[Câu hỏi rút gọn 40 chữ...]", "question": "Nội dung câu hỏi đầy đủ", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "answer": "Đáp án đúng", "details": "Giải thích vì sao đúng (dựa trên kiến thức lịch sử Đảng)" }.
> Yêu cầu định dạng: Tuyệt đối chỉ trả về chuỗi JSON thuần, bắt đầu bằng { và kết thúc bằng }, không bọc trong ```json hay markdown.

---

## III. MÃ LỆNH MẪU GOOGLE CLOUD CLI

Sử dụng Google Cloud CLI để gọi mô hình Gemini 3.1 Pro Preview thông qua REST API.

**Cài đặt Biến môi trường (PowerShell):**
```powershell
$env:PROJECT_ID="tool-dich-thuat"
$env:LOCATION="global"
$env:MODEL_ID="gemini-3.1-pro-preview"
$env:ACCESS_TOKEN=$(gcloud auth print-access-token)
```

**Mẫu lệnh cURL (Gọi Worker 1):**
```powershell
curl.exe -X POST `
  -H "Authorization: Bearer $env:ACCESS_TOKEN" `
  -H "Content-Type: application/json" `
  "https://$env:LOCATION-aiplatform.googleapis.com/v1/projects/$env:PROJECT_ID/locations/$env:LOCATION/publishers/google/models/$env:MODEL_ID:generateContent" `
  -d "{
    \"contents\": [{
      \"role\": \"user\",
      \"parts\": [{
        \"text\": \"COPY_PROMPT_CỦA_WORKER_1_DÁN_VÀO_ĐÂY\"
      }]
    }],
    \"generationConfig\": {
      \"temperature\": 0.2,
      \"maxOutputTokens\": 8192
    }
  }" > phan1_1858_1930.json
```
*(Thay thế đoạn `COPY_PROMPT_...` bằng nội dung Prompt của 9 Worker ở trên để chạy sinh 9 file).*

---

## IV. QUY TRÌNH HỌC TẬP & GHI NHỚ 48 GIỜ (Dựa trên GUI Box Node)
Hệ thống Frontend D3.js đã được cập nhật Box Node siêu lớn có thanh cuộn. Việc đọc JSON sinh ra từ 9 Worker này sẽ biến trình duyệt thành cuốn bách khoa toàn thư.
*   **Giờ 1-12:** Đọc `phan1`, `phan2`, `phan7` (Ra đời Đảng + Giành chính quyền + Tư tưởng Bác Hồ).
*   **Giờ 13-24:** Đọc `phan3`, `phan4`, `phan8` (Kháng chiến Pháp, Mỹ + Ngoại giao quốc tế).
*   **Giờ 25-36:** Đọc `phan5`, `phan6` (Thời kỳ quá độ và CNH-HĐH Đổi mới - Hay ra thi Tự luận nhất).
*   **Giờ 37-48:** Trực tiếp làm `phan9` (Bộ Trắc nghiệm đã chia nhóm 20 câu để chống Lag). Tự giải thích đáp án trên GUI.