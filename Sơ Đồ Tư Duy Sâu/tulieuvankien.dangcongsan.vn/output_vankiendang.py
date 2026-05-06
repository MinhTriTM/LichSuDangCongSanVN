import json
import os

with open('du_lieu_dai_hoi_clean.json', encoding='utf-8') as f:


data = json.load(f)

for dai_hoi in data:


folder_path = dai_hoi['folderName']


os.makedirs(folder_path, exist_ok=True)


for article in dai_hoi['files']:




file_path = os.path.join(folder_path, article['fileName'])




with open(file_path, 'w', encoding='utf-8') as f_out:






f_out.write(article['text'])
