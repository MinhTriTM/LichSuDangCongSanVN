# Q2: Tạo Git Run

## 1. Câu hỏi
tạo 1 filer git_run. mục tiêu trong đó có các file thực thi .bat, khi click file run.bat, nó hỏi đường dẫn thư mục >> nhập đường dẫn thư mục >> hỏi url reponsive.git >> nhập >>  hỏi comment gì cho git commnit >> nhập >> hỏi ... >> tự thực hiện push or pull or clone ... có menu lựa chọn cách dùng git >> từng lựa chọn tương ứng 1 file.bat >> mỗi lựa chọn sẽ thự thi 1 loạt nhiệm vụ của git đối với github...

## 2. Suy nghĩ (Thinking)
- Cần tạo một thư mục `git_run` trong dự án.
- Trong đó có một file `run.bat` đóng vai trò là menu chính, sử dụng lệnh `set /p` để nhận input từ người dùng.
- Từ menu này, người dùng có thể chọn các chức năng: Khởi tạo & Push, Clone, Pull, Push thông thường.
- Mỗi chức năng sẽ gọi một file `.bat` tương ứng (`init_push.bat`, `clone.bat`, `pull.bat`, `push.bat`).
- Các file con này sẽ yêu cầu người dùng nhập các thông tin cần thiết như đường dẫn thư mục `dir_path`, URL repository `git_url`, nội dung commit `commit_msg`... rồi tự động chuyển thư mục bằng `cd /d` và thực thi tuần tự các lệnh Git tương ứng.
- Cần thiết lập bảng mã `chcp 65001` để terminal hiển thị và nhận tiếng Việt không bị lỗi font.
- Ghi log câu hỏi, suy nghĩ và kết quả vào file `Q2_Tao_Git_Run.md` trong thư mục `Lich_Su_Truy_Van` theo đúng yêu cầu dự án.

## 3. Câu trả lời
Đã tạo thư mục `git_run` cùng với file `run.bat` (menu chính) và các file chức năng con tương ứng. Người dùng có thể chạy `run.bat` để sử dụng.
