import os
import json
import sqlite3
import re
from html.parser import HTMLParser

class LSDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {
            "title": "",
            "description": "",
            "events": [],
            "quick_facts": [],
            "related_terms": [],
            "paragraphs": []
        }
        self.current_tag = None
        self.capture_text = False
        self.temp_event = {}
        self.temp_fact = {}
        self.in_h1 = False
        self.in_h2 = False
        self.in_p = False
        self.in_span = False

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        if tag == "title":
            self.capture_text = True
        elif tag == "h1":
            self.in_h1 = True
            self.capture_text = True
        elif tag == "h2":
            self.in_h2 = True
            self.capture_text = True
        elif tag == "p":
            self.in_p = True
            self.capture_text = True
        elif tag == "span" and "font-h3" in attrs_dict.get("class", ""):
            self.capture_text = True
        elif tag == "img":
            alt = attrs_dict.get("data-alt") or attrs_dict.get("alt")
            if alt:
                self.data["description"] += f"\n[Image: {alt}]\n"

    def handle_data(self, data):
        if not self.capture_text:
            return
        
        text = data.strip()
        if not text:
            return

        if self.current_tag == "title":
            self.data["title"] = text
        elif self.in_h1:
            if not self.data["title"]:
                self.data["title"] = text
        elif self.in_h2:
            self.data["paragraphs"].append(text)
        elif self.in_p:
            self.data["paragraphs"].append(text)
        
        # Simple extraction logic for events and facts based on patterns
        if re.match(r"\d{2}/\d{2}/\d{4}", text):
            self.data["events"].append({"date": text, "detail": ""})
        
    def handle_endtag(self, tag):
        if tag == "h1": self.in_h1 = False
        if tag == "h2": self.in_h2 = False
        if tag == "p": self.in_p = False
        self.capture_text = False

def process_directory(base_dir):
    all_data = []
    stitch_dir = os.path.join(base_dir, "stitch_d_ng_th_i_gian_l_ch_s_ng")
    if not os.path.exists(stitch_dir):
        print(f"Directory not found: {stitch_dir}")
        return []

    for folder_name in os.listdir(stitch_dir):
        folder_path = os.path.join(stitch_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
        
        html_path = os.path.join(folder_path, "code.html")
        if not os.path.exists(html_path):
            continue
        
        print(f"Processing {folder_name}...")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        parser = LSDParser()
        parser.feed(html_content)
        
        item = parser.data
        item["folder_id"] = folder_name
        item["description"] = "\n".join(item["paragraphs"])
        all_data.append(item)
    
    return all_data

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved JSON to {output_path}")

def save_to_sqlite(data, output_path):
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS lsd_data")
    cursor.execute("""
        CREATE TABLE lsd_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_id TEXT,
            title TEXT,
            description TEXT,
            events TEXT
        )
    """)
    
    for item in data:
        cursor.execute("""
            INSERT INTO lsd_data (folder_id, title, description, events)
            VALUES (?, ?, ?, ?)
        """, (
            item["folder_id"],
            item["title"],
            item["description"],
            json.dumps(item["events"], ensure_ascii=False)
        ))
    
    conn.commit()
    conn.close()
    print(f"Saved SQLite to {output_path}")

if __name__ == "__main__":
    base_path = r"D:\Download\Thi\LSD\stitch_SDL"
    extracted_data = process_directory(base_path)
    
    if extracted_data:
        save_to_json(extracted_data, os.path.join(base_path, "bd.json"))
        save_to_sqlite(extracted_data, os.path.join(base_path, "database.sqlite"))
    else:
        print("No data extracted.")
