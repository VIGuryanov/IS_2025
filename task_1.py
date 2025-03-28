import requests
import re
from urllib.parse import unquote

#'https://ru.m.wikipedia.org/wiki/
urls = input('Enter urls: ').split(' ')
to_visit = set(urls)
visited = set()
count = 0

with open("index.txt", "a", encoding='utf-8') as index:
    while len(to_visit) != 0 and count < 100:
        url = to_visit.pop()
        visited.add(url)
        domain = re.findall(r'https?://[a-zA-Z0-9.-]*', url)
        if len(domain) == 0:
            continue
        domain = domain[0]        
        resp = requests.get(url)
        text = resp.text
        refs = re.findall(r'<a[^>]*>', text)
        for ref in refs:
            ref = re.findall(r'href="[^"]*"', ref)
            if len(ref) <= 0:
                continue
            ref = ref[0][6:][:-1]
            if len(ref) > 0:
                if ref[0] == '/':
                    ref = domain + ref
                if ref.startswith(domain):
                    if ref not in visited:
                        check_img = ref.split('.')
                        if not (check_img[-1].lower() == 'png' or check_img[-1].lower() == 'jpg' or check_img[-1].lower() == 'jpeg'):
                            to_visit.add(ref)        
        
        text = re.sub(r'<style[^>]*>[^<]*</style>', ' ', text, flags=re.MULTILINE)
        text = re.sub(r'<script[^>]*>(?!.*<script>).*</script>', ' ', text, flags=re.MULTILINE)
        text = re.sub(r'<script[^>]*>[^<]*</script>', ' ', text, flags=re.MULTILINE)

        text = re.sub(r'<mediainfoview[^>]*>(?!.*<mediainfoview>).*</mediainfoview>', ' ', text, flags=re.MULTILINE)

        text = re.sub(r'<[^<>]*>', ' ', text)
        mod2 = re.sub(r'<[^<>]*>', ' ', text)
        while text != mod2:
            text = mod2
            mod2 = re.sub(r'<[^<>]*>', ' ', mod2)

        text = re.sub(r'<[^<>]*>', ' ', text)
        text = re.sub(r'&[^;]*;', ' ', text)
        text = " ".join(text.split())
        text = re.sub(r'[^A-Za-zА-Яа-я0-9 -]', ' ', text)
        text = " ".join(text.split())
        
        
        if len(text.split(' ')) > 1:
            count += 1
            with open(f"web_pages/{count}.txt", "w", encoding='utf-8') as wp:
                wp.write(text)
            
            index.write(f'{count} {unquote(url)}\n')


#превратить ссылки в кирилицу, проверить теги, убрать картинки, разобраться с query