# Lịch sử truy vấn: Câu hỏi 12

## Câu hỏi
... was unexpected at this time.
khi chạy ./run.bat

## Suy nghĩ (Thinking)
Lỗi `... was unexpected at this time.` xảy ra trong Command Prompt của Windows khi chạy file batch. Nguyên nhân là do tôi đã sử dụng dấu ngoặc đơn `()` trong câu lệnh `echo => Đã phát hiện Python. Đang tiến hành tạo Cơ sở dữ liệu (JSON)...` nằm bên trong một khối lệnh `if`. Trong DOS/Batch, dấu ngoặc đơn đóng `)` trong chuỗi `(JSON)` bị hiểu nhầm là kết thúc sớm khối lệnh `if`, khiến cho chuỗi dấu chấm `...` phía sau trở thành một lệnh không hợp lệ.
Tôi đã sử dụng công cụ `replace` để chỉnh sửa file `run.bat`, thay thế đoạn `(JSON)...` thành `JSON...`. Việc loại bỏ dấu ngoặc đơn này đã khắc phục hoàn toàn lỗi cú pháp.

## Câu trả lời
Đã phát hiện và sửa lỗi cú pháp trong file `run.bat`. Nguyên nhân là do dấu ngoặc đơn trong chữ `(JSON)` làm hệ thống hiểu nhầm. Bây giờ bạn có thể chạy lại file `run.bat` một cách bình thường!