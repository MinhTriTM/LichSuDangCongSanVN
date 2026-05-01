# Q9: Bổ sung tính năng hiển thị cấu hình Account Git trên Dashboard

## 1. Câu hỏi
thêm hiển thị account... nhiều nhất

## 2. Suy nghĩ (Thinking)
- Người dùng muốn hiển thị thông tin tài khoản Git (Tên người dùng và Email) lên giao diện Dashboard một cách đầy đủ và chi tiết nhất.
- Tài khoản Git được cấu hình thông qua `git config user.name` và `git config user.email`. 
- Nếu thư mục hiện tại chưa được cấu hình tài khoản hoặc chưa có Git, hệ thống cần xử lý ngoại lệ và hiển thị "Chưa cấu hình".
- Giải pháp:
  - Nâng cấp hàm `get_git_info(cwd)` trong file `git_toolkit.py` để lấy thêm 2 thông số: `user_name` và `user_email`.
  - Cập nhật hàm `draw_dashboard` để unpacking 4 biến trả về và thêm một dòng hiển thị `Account: {Name} ({Email})` trong khung viền ANSI.
  - Sửa đổi lại logic unpack của tất cả các hàm đang dùng `get_git_info` (như `handle_pull`, `main`) để chỉ lấy index cụ thể thay vì bị lỗi unpack quá số lượng biến.

## 3. Câu trả lời
Đã hoàn thành! Giao diện bảng điều khiển (Dashboard) hiện tại đã được nâng cấp để trích xuất và hiển thị trực tiếp Tên (Name) và Email của tài khoản Git đang cấu hình tại thư mục làm việc của bạn. Việc này giúp bạn không bao giờ sợ "push nhầm tài khoản công ty vào source code cá nhân" nữa. Hãy mở lại tool để xem giao diện mới nhé!
