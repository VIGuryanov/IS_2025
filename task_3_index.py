import os
import json

rev_index = {}

files = os.listdir('tokens')
files = list(map(lambda x: int(x.split('.')[0]), files))
files.sort()

for file in files:
    with open(f"tokens/{file}.txt", "r", encoding='utf-8') as page:
        tokens = page.read().split()

    for token in tokens:
        if not token in rev_index:
            rev_index[token] = set()
        rev_index[token].add(file)
    
    with open(f"count.txt", "a", encoding='utf-8') as counts: 
        counts.write(f'{len(tokens)}\n')

new_dict = {}
for key, value in rev_index.items():
    new_dict[key] = list(value)
    new_dict[key].sort()

rev_index = dict(sorted(new_dict.items()))
with open(f"rev_index.txt", "w", encoding='utf-8') as page:    
    page.write(json.dumps(rev_index, ensure_ascii=False))