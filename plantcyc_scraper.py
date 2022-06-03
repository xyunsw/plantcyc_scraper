import sys
import os
import re
import time
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup

# os.environ['http_proxy'] = 'http://127.0.0.1:10801'
# os.environ['https_proxy'] = 'http://127.0.0.1:10801'

def make_url(id_):
    id_ = urllib.parse.quote_plus(id_)
    return f'https://pmn.plantcyc.org/compound?orgid=PLANT&id={id_}'

def make_valud_filename(name):
    return re.sub(r':', '_', name)

def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <ID_file>', file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        ids = []
        for line in f:
            line = line.strip()
            if line != '':
                ids.append(line)
    try:
        os.mkdir('pages')
    except FileExistsError:
        pass
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8')as f:
            data = json.load(f)
    else:
        data = {}
    ses = requests.sessions.Session()
    try:
        for id_ in ids:
            # print(f'handling {id_}')
            if id_ in data:
                continue
            url = make_url(id_)
            filename = make_valud_filename(id_) + '.html'
            page_file = f'pages/{filename}'
            if os.path.exists(page_file):
                with open(page_file, encoding='utf-8') as f:
                    content = f.read()
            else:
                res = ses.get(url)
                if not res.ok:
                    print(res.text)
                    raise ValueError(f'Server returned a bad response: {res}')
                else:
                    content = res.text
                    with open(page_file, 'w', encoding='utf-8') as f:
                        f.write(content)
            soup = BeautifulSoup(content, 'html.parser')
            res = soup.find_all('font', class_='header')
            elem = res[0]
            name = elem.decode_contents()
            name = name.strip()
            res = soup.find_all('td', string='\nChemical Formula')
            if (len(res)) == 0:
                formula = ''
            else:
                elem = res[0]
                elem = elem.find_next_sibling()
                formula = elem.decode_contents()
                formula = formula.strip()
            print(name, formula)
            data[id_] = {
                'name': name,
                'formula': formula,
                'url': url
            }
            print(f'{id_}: {name} {formula}')
            time.sleep(0.5)
            # break
    finally:
        with open('data.json', 'w', encoding='utf-8')as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    

if __name__ == "__main__":
    main()
