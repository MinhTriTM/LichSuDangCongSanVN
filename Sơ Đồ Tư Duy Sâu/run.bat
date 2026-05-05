@echo off
chcp 65001 >nul
title Server Quan Ly: lsd.minhtritm.id.vn
color 0A

echo ====================================================================
echo      HỆ THỐNG MÁY CHỦ CỤC BỘ (CHẠY TRỰC TIẾP QUA PORT 3000)
echo ====================================================================
echo Domain đích: http://lsd.minhtritm.id.vn/
echo IP Local: 192.168.1.100:3000
echo Thư mục gốc: %CD%
echo.

REM Tự động đổi tên thư mục để khớp với URL Path
if exist "mindmap-app\" (
    echo Đang đổi tên thư mục dự án thành LSD...
    ren "mindmap-app" "LSD"
)

if not exist "LSD\index.html" (
    echo [LỖI] Không tìm thấy thư mục LSD chứa mã nguồn dự án.
    echo Vui lòng đảm bảo file run.bat nằm cùng cấp với thư mục LSD.
    pause
    exit
)

echo [1/2] Đang chuẩn bị dữ liệu và khởi động Web Server tại cổng 3000...
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo =^> Đã phát hiện Python. Đang tiến hành tạo Cơ sở dữ liệu JSON...
    cd LSD
    python build_db.py
    cd ..
    echo =^> Đã tạo xong CSDL. Đang chạy HTTP Server...
    start "Web Server (Python)" cmd /c "title Web Server (Port 3000) & python -m http.server 3000"
    goto success
)

node -v >nul 2>&1
if %errorlevel% equ 0 (
    echo =^> Đã phát hiện Node.js. Đang chạy npx serve...
    start "Web Server (Node)" cmd /c "title Web Server (Port 3000) & npx serve -l 3000"
    goto success
)

color 0E
echo [CẢNH BÁO] Không tìm thấy Python hoặc Node.js trên máy này!
echo.
echo ĐỂ CHẠY TRÊN MÁY 1:
echo 1. Cài đặt Python hoặc Node.js trên Máy 1.
echo 2. Hoặc cấu hình Nginx chạy ở port 3000 và trỏ vào thư mục này.
pause
exit

:success
echo.
echo [2/2] Web Server đã chạy ngầm ở Port 3000!
echo ====================================================================
echo HƯỚNG DẪN CẤU HÌNH CHO MÁY 1 (IP: 192.168.1.100):
echo 1. Đảm bảo thư mục này đã được copy qua Máy 1 và file này đang chạy trên Máy 1.
echo 2. Đảm bảo Modem/Router đã NAT (Mở port): 
echo    - Cổng bên ngoài (External Port): 80 (hoặc tùy bạn)
echo    - Cổng bên trong (Internal Port): 3000
echo    - IP Nội bộ (Internal IP): 192.168.1.100
echo 3. Lấy IP Public của Máy 1 (lên google gõ "what is my ip").
echo 4. Vào trang quản lý tên miền minhtritm.id.vn, tạo bản ghi DNS:
echo    - Loại: A
echo    - Tên (Name): lsd
echo    - Giá trị (Value): [IP Public của Máy 1]
echo 5. Mọi người có thể truy cập bằng tên miền:
echo    =^> http://lsd.minhtritm.id.vn/
echo    (Web sẽ tự động chuyển hướng vào /LSD/)
echo ====================================================================
echo Nhấn phím bất kỳ để xem thử trên máy local này tại: http://localhost:3000/
pause >nul
start http://localhost:3000/
