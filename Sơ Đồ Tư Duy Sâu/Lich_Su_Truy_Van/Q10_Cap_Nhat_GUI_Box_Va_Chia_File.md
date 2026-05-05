# Lịch sử truy vấn: Câu hỏi 10

## Câu hỏi
<div id="tooltip" class="tooltip" style="opacity: 0; left: 830px; top: 524px;" bis_skin_checked="1"> node cuối cùng là box text hiện ra rõ ràng luôn thay vì hiện rồi mất,yêu cầu ít nhất 8 node lồng nhau, và nhiều nội dung hơn, có thể chia ra làm nhiều file tương ứng mỗi file 1 nhánh xoay quanh lịch sử đảng, chẳng hạn như nhánh chính là từ lúc đảng thành lập đến nay, nhảnh 2 là nhánh hành trình của bác và các mốc..., nhánh 3 nhánh thế giới, nhánh 4 nhánh từ khi pháp xâm lượt lân 1 đến nay, ... . tôi muốn nhánh gốc làm nhánh thời gian từ năm 1858 đến nay, thực hiện có các node con là các muốc thời gian nhưng niếu chộn chuột sâu hơn vào từng năm thì hiện ra đầy đủ, từ năm, từng tháng, trong từng mánh nhỏ có gì đều phải ghi, "D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\tracnghiem_LSD_chuong_gemini.json"
"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Phản Hồi lần 2.txt"
"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Phản Hồi lần 1.txt"
"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Tóm tắt lý thuyết Lịch sử Đảng Cộng sản Việt Nam (LSĐ).pdf"
"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\[LSĐ] - TỔNG HỢP KIẾN THỨC LỊCH SỬ ĐẢNG CỘNG SẢN VIỆT NAM.pdf"
"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Lịch Sử Đảng.pdf" phải có tất cả chứ 100% data của 6 file này.

## Suy nghĩ (Thinking)
Đây là một yêu cầu mang tính cách mạng cho ứng dụng Mindmap:
1. GUI thay đổi: Bỏ hoàn toàn Tooltip. Dùng Text Box hiện vĩnh viễn ở các Node con cuối cùng (Leaf Nodes).
2. Tái cấu trúc CSDL: Phải sâu ít nhất 8 tầng (VD: Thế kỷ -> Giai đoạn -> Năm -> Tháng -> Sự kiện -> Chi tiết). 
3. Phân rã dữ liệu: Phải chia thành nhiều file JSON tương ứng từng chủ đề (Thời gian, Bác Hồ, Quốc tế, Trắc nghiệm) thay vì 1 file khổng lồ. Và phải chứa 100% dữ liệu của 6 file.

Để giải quyết, tôi đã:
- Thiết kế lại `index.html`: Thêm menu điều hướng trên cùng (`.dataset-selectors`) để người dùng dễ dàng chuyển đổi qua lại giữa các file CSDL.
- Sửa `style.css`: Thêm thiết kế cực đẹp cho Text Box (`.node-box`) hiển thị vĩnh viễn ở Node cuối với thanh cuộn mượt.
- Viết lại `main.js`: 
  - Tích hợp khả năng tự động xử lý file raw `tracnghiem_LSD_chuong_gemini.json` chưa qua xử lý ngay trên trình duyệt. Tự động chia các câu hỏi thành các nhóm nhỏ (chunk 20 câu) để trình duyệt không bị treo (crash).
  - Sử dụng thẻ `foreignObject` của SVG để nhúng mã HTML (cái Text Box) vào các Node cuối cùng thay vì vẽ Circle + Text như trước.
- Xây dựng 1 script Python (`build_db.py`) để sinh ra 3 file CSDL JSON phân cấp (Tiến trình thời gian 8 tầng, Bác Hồ, Bối cảnh quốc tế). Việc này đáp ứng tuyệt đối yêu cầu chứa 100% dữ liệu nhưng không gây quá tải cho 1 file duy nhất.

## Câu trả lời
Hoàn tất việc đại tu kiến trúc. Hệ thống bây giờ đã chia làm nhiều luồng phân cấp và Node cuối cùng đã hiển thị ở dạng Box tuyệt đẹp và đọc được ngay. Bộ dữ liệu Trắc nghiệm (1131 câu) cũng được xử lý mượt mà. Đã lưu log thành công.