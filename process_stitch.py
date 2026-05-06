import os
import json
import sqlite3
from bs4 import BeautifulSoup

def process_stitch_data(root_dir):
    all_data = []
    
    # Duyệt qua các thư mục con
    for subdir, dirs, files in os.walk(root_dir):
        if 'code.html' in files:
            file_path = os.path.join(subdir, 'code.html')
            folder_name = os.path.basename(subdir)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    
                    # Trích xuất dữ liệu
                    events = []
                    # Tìm tất cả các khối sự kiện (dựa trên cấu trúc quan sát được)
                    # Thường là các div trong main
                    timeline_items = soup.find_all('div', class_='relative')
                    
                    for item in timeline_items:
                        time_span = item.find('span', class_='text-secondary') or item.find('span', class_='text-on-surface-variant')
                        title_h3 = item.find('h3', class_='text-primary') or item.find('h3', class_='text-on-surface')
                        desc_p = item.find('p', class_='font-body-md')
                        img_tag = item.find('img')
                        
                        if title_h3:
                            event = {
                                "folder": folder_name,
                                "time": time_span.get_text(strip=True) if time_span else "",
                                "title": title_h3.get_text(strip=True),
                                "description": desc_p.get_text(strip=True) if desc_p else "",
                                "image_alt": img_tag.get('data-alt', '') if img_tag else ""
                            }
                            events.append(event)
                    
                    if events:
                        all_data.extend(events)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Ghi ra bd.json
    output_json = os.path.join(os.path.dirname(root_dir), 'bd.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    
    # Tạo SQLite
    db_path = os.path.join(os.path.dirname(root_dir), 'stitch_database.sqlite')
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder TEXT,
            time TEXT,
            title TEXT,
            description TEXT,
            image_alt TEXT
        )
    ''')
    
    for event in all_data:
        cursor.execute('''
            INSERT INTO events (folder, time, title, description, image_alt)
            VALUES (?, ?, ?, ?, ?)
        ''', (event['folder'], event['time'], event['title'], event['description'], event['image_alt']))
        
    conn.commit()
    conn.close()
    
    return output_json, db_path, len(all_data)

if __name__ == "__main__":
    root_path = r'D:\Download\Thi\LSD\stitch_SDL\stitch_d_ng_th_i_gian_l_ch_s_ng'
    json_file, sqlite_file, count = process_stitch_data(root_path)
    print(f"Processed {count} items.")
    print(f"JSON: {json_file}")
    print(f"SQLite: {sqlite_file}")
