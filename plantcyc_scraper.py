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

def make_summary_url(id_):
    id_ = urllib.parse.quote_plus(id_)
    return f'https://pmn.plantcyc.org/cpd-tab?orgid=PLANT&id={id_}&tab=SUMMARY'

def make_wg_url(path):
    return 'https://pmn.plantcyc.org' + path

def make_valid_filename(name):
    return re.sub(r':|\/', '_', name)

def get_table_row_content(soup, row_name):
    res = soup.find_all('td', string=row_name)
    if (len(res)) == 0:
        value = ''
    else:
        elem = res[0]
        elem = elem.find_next_sibling()
        value = elem.decode_contents()
        value = value.strip()
    return value

def get_page(ses, ns, id_, **extra):
    reload = extra.get('reload', False)
    if not ns:
        url = make_url(id_)
    elif ns == 'summary':
        url = make_summary_url(id_)
    elif ns == 'webgraphics':
        url = make_wg_url(extra['path'])
        # print(f'wg url is: {url}')
    else:
        raise NotImplementedError()
    
    filename = make_valid_filename(id_) + '.html'
    page_dir = 'pages'
    if ns:
        page_dir += '/' + ns
    try:
        os.makedirs(page_dir)
    except FileExistsError:
        pass
    page_file = f'{page_dir}/{filename}'
    if os.path.exists(page_file) and not reload:
        with open(page_file, encoding='utf-8') as f:
            content = f.read()
    else:
        if ns == 'webgraphics':
            # we have to request the main page so that server generates webgraphics data
            get_page(ses, None, id_, reload=True)
        res = ses.get(url)
        if not res.ok:
            print(res.text)
            print('url: ', res.url)
            raise ValueError(f'Server returned a bad response: {res}')
        else:
            content = res.text
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(content)
    return content

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
            print(f'processing {id_}...')
            url = make_url(id_)
            content = get_page(ses, None, id_)
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
            
            summary_content = get_page(ses, 'summary', id_)
            summary_soup = BeautifulSoup(summary_content, 'html.parser')
            res = summary_soup.find_all('td', string='\nSynonyms')
            if len(res) == 0:
                synonyms = ''
            else:
                elem = res[0]
                elem = elem.find_next_sibling()
                synonyms = elem.decode_contents()
                synonyms = synonyms.strip()

            smiles = get_table_row_content(summary_soup, '\nSMILES')
            inchi = get_table_row_content(summary_soup, '\nInChI')

            res = summary_soup.select('.summaryText h3')
            if len(res) == 0:
                summary = ''
            else:
                elem = res[0]
                elem = elem.next_sibling
                summary = elem.strip()

            chebi = get_table_row_content(summary_soup, '\nChEBI')
            kegg = get_table_row_content(summary_soup, '\nKegg')
            pubchem = get_table_row_content(summary_soup, '\nPubChem')
            refmet = get_table_row_content(summary_soup, '\nRefMet')

            res = re.search(r'\/\S+\.wg', content)
            if not res:
                webgraphics_data = ''
            else:
                wg_path = res.group(0)
                webgraphics_data = get_page(ses, 'webgraphics', id_, path=wg_path)

            data[id_] = {
                'name': name,
                'formula': formula,
                'synonyms': synonyms,
                'smiles': smiles,
                'inchi': inchi,
                'summary': summary,
                'chebi': chebi,
                'kegg': kegg,
                'pubchem': pubchem,
                'refmet': refmet,
                'webgraphics_data': webgraphics_data,
                'url': url
            }
            print(f'{id_}: {name} {formula}')
            # time.sleep(0.5)
            # break
    finally:
        with open('data.json', 'w', encoding='utf-8')as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    

if __name__ == "__main__":
    main()
