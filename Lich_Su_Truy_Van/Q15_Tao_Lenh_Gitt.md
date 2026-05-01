# Q15: Tạo lệnh `gitt` gọi nhanh từ CMD

## 1. Câu hỏi
muốn ở cmd gõ gitt thì nó tự mở @git_run\Run_Windows.bat

## 2. Suy nghĩ (Thinking)
- Người dùng muốn tạo một alias (lệnh gõ tắt) là `gitt` để khởi chạy Tool thông qua CMD.
- Khi người dùng gõ `gitt` từ một thư mục khác, CMD sẽ tìm file `gitt.bat` hoặc `gitt.exe` trong thư mục hiện tại hoặc trong biến môi trường PATH.
- Nếu tạo file `gitt.bat` gọi đến file `Run_Windows.bat`, thì file `Run_Windows.bat` cũng phải được cập nhật lại để có thể tự tìm thấy file `git_toolkit.py` của nó bất kể người dùng đang đứng ở thư mục nào (đường dẫn tương đối `%~dp0`).
- **Thực hiện:**
  1. Cập nhật `git_run/Run_Windows.bat`: Đổi `python git_toolkit.py %*` thành `python "%~dp0git_toolkit.py" %*`. Biến `%~dp0` sẽ luôn lấy đường dẫn gốc chứa file `.bat` đó.
  2. Tạo file `gitt.bat` tại thư mục ngoài cùng (D:\Download\Thi\LSD) với nội dung: `call "%~dp0git_run\Run_Windows.bat" %*`.
- Nếu người dùng muốn lệnh `gitt` chạy được trên **toàn bộ máy tính (mọi thư mục)** thì phải hướng dẫn họ copy file `gitt.bat` này bỏ vào ổ `C:\Windows` hoặc thêm thư mục chứa nó vào Environment Variables.

## 3. Câu trả lời
Tuyệt vời! Tôi đã tạo xong file `gitt.bat` ở thư mục ngoài cùng và nâng cấp đường dẫn thông minh cho Tool.
Từ bây giờ, bạn chỉ cần mở CMD ở thư mục `LSD` này và gõ `gitt`, giao diện Git Easy Toolkit sẽ lập tức hiện ra!

*(Lưu ý: Nếu bạn muốn gõ `gitt` ở BẤT KỲ THƯ MỤC NÀO trên toàn bộ máy tính mà nó vẫn chạy, bạn chỉ việc copy file `gitt.bat` và dán thẳng vào thư mục `C:\Windows` là xong. Windows sẽ tự nhận diện lệnh đó thành lệnh hệ thống!)*
