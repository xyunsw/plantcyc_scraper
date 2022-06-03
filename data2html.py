import json
import sys

html_template = '''
<!DOCTYPE html>
<html>
    <head>
        <title>output</title>
    </head>
    <body>
        <table>
            <tbody>
                %s
            </tbody>
        </table>
    </body>
</html>
'''

def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <data_json file> <output_html file>', file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)
    trs = []
    for id_ in data:
        tr = f'''<tr>
            <td>{id_}</td>
            <td>{data[id_]["name"]}</td>
            <td>{data[id_]["formula"]}</td>
            <td> <a href="{data[id_]["url"]}">{data[id_]["url"]}</a></td>
        </tr>'''
        trs.append(tr)
    tr_html = ''.join(trs)
    html = html_template % tr_html
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()

    
