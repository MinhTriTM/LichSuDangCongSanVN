# Lịch sử truy vấn: Câu hỏi 14

## Câu hỏi
viết prompt kèm theo cho từng luồn.

## Suy nghĩ (Thinking)
Người dùng yêu cầu viết sẵn các Prompt cụ thể cho 9 luồng (Workers) để chuẩn bị chạy mô hình Gemini 3.1 Pro Preview qua Vertex AI.
Mục tiêu là biến những Prompt này thành một cỗ máy sinh dữ liệu tự động, vừa bao quát toàn bộ lịch sử, vừa đáp ứng chuẩn xác định dạng JSON cho ứng dụng Web. 
Tôi đã tiến hành chỉnh sửa và ghi đè file `KeHoachHoanThanh_DaLuong.md`. Trong file này, tôi đã xây dựng 9 đoạn Prompt đóng vai trò (Role-prompting) là "Giáo sư Lịch sử Đảng". Mỗi Prompt được thiết kế để:
1. Giao ranh giới thời gian rõ ràng (tránh AI sinh dữ liệu trùng lặp).
2. Liệt kê rõ những sự kiện, hội nghị, nghị quyết, bài học kinh nghiệm BẮT BUỘC phải bóc tách.
3. Ràng buộc khắt khe định dạng đầu ra: cấu trúc cây (Hierarchy), độ sâu 8 tầng, JSON thuần (không dùng markdown code block ` ```json `), và nội dung chi tiết phải đạt độ dài 150-300 chữ để đáp ứng nhu cầu phân tích chuyên sâu.

Việc thiết kế Prompt như vậy giúp người dùng chỉ cần "Copy và Paste" là có thể tạo ra CSDL bách khoa toàn thư mà không sợ AI bị "ảo giác" (hallucination) hay sinh sai cấu trúc.

## Câu trả lời
Tôi đã bổ sung toàn bộ 9 Prompt siêu chi tiết vào bản Kế hoạch hoàn thành. Các Prompt đã được thiết kế dưới góc độ "Kỹ sư Prompt" (Prompt Engineering) với các ràng buộc chặt chẽ về định dạng JSON, độ sâu 8 tầng và liệt kê rõ ràng các sự kiện lịch sử không thể thiếu. Bạn có thể mở file Kế hoạch lên để sao chép ngay lập tức.