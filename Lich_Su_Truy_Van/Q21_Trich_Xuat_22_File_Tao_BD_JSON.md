# Truy vấn Q21: Trích xuất nội dung từ 22 file code.html và tạo bd.json

## Câu hỏi
Tôi đã trích xuất nội dung từ 22 file code.html trong thư mục 'D:\Download\Thi\LSD\stitch_SDL\stitch_d_ng_th_i_gian_l_ch_s_ng'. 
Hãy dựa vào kiến thức trong các file này để tạo ra file 'D:\Download\Thi\LSD\stitch_SDL\bd.json'.

## Suy nghĩ
1. Liệt kê 22 thư mục con.
2. Đọc nội dung file `code.html` trong mỗi thư mục để lấy tiêu đề, mô tả và các sự kiện/mốc thời gian.
3. Sử dụng regex và các kỹ thuật xử lý văn bản để trích xuất dữ liệu chính xác.
4. Tổng hợp dữ liệu vào cấu trúc JSON theo yêu cầu.
5. Ghi file `bd.json` với encoding `utf-8-sig`.
6. Giải thích về hạn chế môi trường shell và cung cấp giải pháp script Python.

## Câu trả lời
Đã hoàn thành việc trích xuất dữ liệu từ 22 thư mục và tạo file `D:\Download\Thi\LSD\stitch_SDL\bd.json`. 
Do hạn chế của môi trường shell (không có sẵn thư viện sqlite3 hoặc quyền thực thi tương ứng), tôi không thể tạo trực tiếp file .sqlite. Tuy nhiên, tôi đã kiểm tra và xác nhận script 'complete_stitch.py' có sẵn trong thư mục để bạn tự chạy và chuyển đổi từ JSON sang SQLite.
