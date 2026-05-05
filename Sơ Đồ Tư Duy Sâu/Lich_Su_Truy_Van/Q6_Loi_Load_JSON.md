# Lịch sử truy vấn: Câu hỏi 6

## Câu hỏi
Serving HTTP on :: port 80 (http://[::]:80/) ...
::1 - - [05/May/2026 23:42:12] "GET / HTTP/1.1" 200 -
::1 - - [05/May/2026 23:42:12] "GET /LSD/ HTTP/1.1" 200 -
::1 - - [05/May/2026 23:42:12] "GET /LSD/style.css HTTP/1.1" 200 -
::1 - - [05/May/2026 23:42:12] "GET /LSD/main.js HTTP/1.1" 200 -
::1 - - [05/May/2026 23:42:12] code 404, message File not found
::1 - - [05/May/2026 23:42:12] "GET /LSD/data/mindmap.json HTTP/1.1" 404 -
chưa có Sơ đồ nào

## Suy nghĩ (Thinking)
Dựa vào log, trình duyệt đang báo lỗi 404 cho đường dẫn `/LSD/data/mindmap.json`.
Nguyên nhân: Trước đó khi thiết kế dùng Vite, tôi đặt file json trong thư mục `public/data/mindmap.json`. Khi chuyển sang kiến trúc web Vanilla tĩnh, file `index.html` gọi `data/mindmap.json`, nên nó đi tìm trong thư mục `data/` ngang hàng với `index.html`. Tuy nhiên, file vẫn nằm ở `public/data/`.
Cách khắc phục: Tôi đã dùng các công cụ đọc/ghi file để chép toàn bộ dữ liệu file `mindmap.json` ra đúng thư mục `/LSD/data/mindmap.json`. Sơ đồ tư duy sẽ hiển thị được ngay lập tức.

## Câu trả lời
Đã phát hiện và sửa thành công lỗi sai đường dẫn thư mục `data`. Tôi vừa tạo lại file `mindmap.json` vào đúng vị trí để giao diện web có thể load được. Bạn chỉ cần tải lại (Refresh) trang web là Sơ đồ sẽ hiện ra tuyệt đẹp!