import os
import re
import json
import sqlite3

root_dir = r'D:\Download\Thi\LSD\stitch_SDL\stitch_d_ng_th_i_gian_l_ch_s_ng'
data = []

if not os.path.exists(root_dir):
    print(f"Error: Directory {root_dir} not found.")
    exit(1)

for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        html_path = os.path.join(folder_path, 'code.html')
        if os.path.exists(html_path):
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                title_match = re.search(r'<title>(.*?)</title>', content)
                title = title_match.group(1).strip() if title_match else folder
                
                # Extract h2, h3, p content
                texts = re.findall(r'<(?:h2|h3|p)[^>]*>(.*?)</(?:h2|h3|p)>', content, re.DOTALL)
                clean_texts = [re.sub(r'<.*?>', '', t).strip() for t in texts if t.strip()]
                
                # Extract images
                images = re.findall(r'<img[^>]+src=\"(.*?)\"', content)
                
                data.append({
                    'folder': folder,
                    'title': title,
                    'content': clean_texts,
                    'images': images
                })
            except Exception as e:
                print(f"Warning: Could not process {html_path}: {e}")

# Save to db.json
json_output_path = os.path.join(root_dir, 'bd.json')
with open(json_output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Save to database.sqlite
db_path = os.path.join(root_dir, 'database.sqlite')
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('CREATE TABLE stitch_data (id INTEGER PRIMARY KEY, folder TEXT, title TEXT, content TEXT, images TEXT)')

for entry in data:
    cursor.execute('INSERT INTO stitch_data (folder, title, content, images) VALUES (?, ?, ?, ?)', 
                   (entry['folder'], entry['title'], '\n'.join(entry['content']), json.dumps(entry['images'], ensure_ascii=False)))

conn.commit()
conn.close()

print(f"Successfully processed {len(data)} folders.")
print(f"JSON saved to: {json_output_path}")
print(f"SQLite saved to: {db_path}")
