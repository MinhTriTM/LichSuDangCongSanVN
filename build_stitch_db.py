import sqlite3
import json
import os
import re

# Đường dẫn các file nguồn
BASE_DIR = r"D:\Download\Thi\LSD"
SOURCE_MD = os.path.join(BASE_DIR, "DAI_CO_SO_DU_LIEU_LICH_SU_DANG.md")
SOURCE_JSON = os.path.join(BASE_DIR, "lichsudang.json")
OUTPUT_SQLITE = os.path.join(BASE_DIR, "stitch_SDL", "db.sqlite")
OUTPUT_JSON = os.path.join(BASE_DIR, "stitch_SDL", "db.json")

def parse_md_to_events(md_path):
    events = []
    current_section = ""
    current_chapter = ""
    
    with open(md_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if line.startswith("## PHẦN"):
            current_section = line.replace("#", "").strip()
        elif line.startswith("### CHƯƠNG"):
            current_chapter = line.replace("#", "").strip()
        elif line.startswith("- **") or line.startswith("* **"):
            # Tìm kiếm mốc thời gian và nội dung
            match = re.match(r"[-*]\s*\*\*(.*?)\*\*:\s*(.*)", line)
            if match:
                time_point = match.group(1)
                content = match.group(2)
                events.append({
                    "section": current_section,
                    "chapter": current_chapter,
                    "time": time_point,
                    "content": content
                })
    return events

def create_db():
    print("Bắt đầu parse dữ liệu từ Markdown...")
    events = parse_md_to_events(SOURCE_MD)
    
    # Load thêm dữ liệu từ JSON hiện có nếu có
    if os.path.exists(SOURCE_JSON):
        try:
            with open(SOURCE_JSON, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                # Giả sử cấu trúc JSON là một list các object
                if isinstance(old_data, list):
                    for item in old_data:
                        events.append({
                            "section": "Dữ liệu JSON",
                            "chapter": item.get("chapter", ""),
                            "time": item.get("time", ""),
                            "content": item.get("content", item.get("question", ""))
                        })
        except Exception as e:
            print(f"Lỗi load JSON: {e}")

    # Tạo SQLite
    print(f"Đang tạo SQLite tại {OUTPUT_SQLITE}...")
    if not os.path.exists(os.path.dirname(OUTPUT_SQLITE)):
        os.makedirs(os.path.dirname(OUTPUT_SQLITE))
        
    conn = sqlite3.connect(OUTPUT_SQLITE)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS history_events")
    cursor.execute("""
        CREATE TABLE history_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT,
            chapter TEXT,
            time_point TEXT,
            content TEXT
        )
    """)
    
    for ev in events:
        cursor.execute("INSERT INTO history_events (section, chapter, time_point, content) VALUES (?, ?, ?, ?)",
                       (ev['section'], ev['chapter'], ev['time'], ev['content']))
    
    conn.commit()
    conn.close()
    
    # Tạo JSON tổng hợp
    print(f"Đang tạo JSON tại {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=4)
        
    print("Hoàn thành!")

if __name__ == "__main__":
    create_db()
