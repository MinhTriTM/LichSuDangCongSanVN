# Q13: Tổng hợp các lệnh Git đã tích hợp trong Tool

## 1. Câu hỏi
hiện có các lệnh nào rồi

## 2. Suy nghĩ (Thinking)
- Người dùng muốn biết Tool hiện tại đang hỗ trợ cụ thể những lệnh Git nào sau đợt nâng cấp toàn diện.
- Dựa trên mã nguồn `git_toolkit.py` đã hoàn thiện, tôi sẽ liệt kê chi tiết các lệnh thực tế được gọi dưới nền để người dùng thấy được độ "Pro" của công cụ.
- Các lệnh được phân bổ theo 6 Menu chính:
  1. Cấu hình: `init`, `clone`, `remote add`, `config user`
  2. Flow: `pull` (có xử lý conflict), `status`, `add .` + `commit` + `push`
  3. Branch: `branch -a`, `checkout -b`, `checkout`, `merge`, `branch -d`
  4. Kiểm tra: `log --graph`, `diff`, `show`, `blame`
  5. Sửa lỗi: `restore` + `clean`, `stash`, `stash pop`, `commit --amend`, `reset --soft`, `reset --hard`, `revert`
  6. Nâng cao: `tag -a`, `cherry-pick`

## 3. Câu trả lời
(Liệt kê chi tiết danh sách các lệnh cho người dùng xem)
