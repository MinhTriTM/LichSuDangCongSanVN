import os
import json
import re

base_dir = r'D:\Download\Thi\LSD\stitch_SDL\stitch_d_ng_th_i_gian_l_ch_s_ng'
output_file = r'D:\Download\Thi\LSD\stitch_SDL\bd.json'

data = []

if not os.path.exists(base_dir):
    print(f"Error: Directory {base_dir} does not exist.")
    exit(1)

folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

for folder in folders:
    file_path = os.path.join(base_dir, folder, 'code.html')
    if not os.path.exists(file_path):
        continue
    
    content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        try:
            with open(file_path, 'r', encoding='utf-16') as f:
                content = f.read()
        except Exception:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
    
    title_match = re.search(r'<title>(.*?)</title>', content, re.S)
    title = title_match.group(1).strip() if title_match else folder
    
    # Clean HTML tags helper
    def clean_html(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.strip()

    # Extract description
    description = ""
    desc_patterns = [
        r'<p class="[^"]*body-lg[^"]*">(.*?)</p>',
        r'<p class="[^"]*body-md[^"]*">(.*?)</p>',
        r'<p>(.*?)</p>'
    ]
    for p in desc_patterns:
        m = re.search(p, content, re.S)
        if m:
            description = clean_html(m.group(1))
            if description: break

    events = []
    # Find dates and details
    # Common patterns in the provided files
    # 1. <div class="font-h2 text-h2 text-secondary mb-2">3/2/1930</div>
    # 2. <h3 class="font-h3 text-h3 text-primary">1930</h3>
    # 3. <h2 class="font-h1 text-h1 text-primary">Thời kỳ 1930 - 1945</h2>
    
    # Pattern for dates in div/h2/h3
    pattern = re.compile(r'<(h[1-3]|div)[^>]*?>\s*([^<]{4,50})\s*</\1>', re.S)
    matches = list(pattern.finditer(content))
    
    found_dates = set()
    for i, m in enumerate(matches):
        tag = m.group(1)
        text = m.group(2).strip()
        
        # Check if text contains a year
        if re.search(r'\b(18|19|20)\d{2}\b', text):
            # Find next paragraph for detail
            start_search = m.end()
            # If there's a next match, limit search to before it
            end_search = matches[i+1].start() if i + 1 < len(matches) else len(content)
            
            detail_match = re.search(r'<p[^>]*?>(.*?)</p>', content[start_search:end_search], re.S)
            detail = clean_html(detail_match.group(1)) if detail_match else ""
            
            if text not in found_dates:
                events.append({'date': text, 'detail': detail})
                found_dates.add(text)

    data.append({
        'folder_id': folder,
        'title': title,
        'description': description,
        'events': events
    })

# Write JSON with utf-8-sig
with open(output_file, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully processed {len(data)} folders.")
