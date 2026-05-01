@echo off
REM Chuyển đến thư mục chứa script Python
cd /d "%~dp0"
REM Chạy script Python
python extract_text.py
pause