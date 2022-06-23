import json
import sys
from html import escape

html_template = '''
<!DOCTYPE html>
<html>
    <head>
        <title>output</title>
    </head>
    <body>
        <h2>Output</h2>
        <div>webgraphics script begin</div>
        <script src="https://pmn.plantcyc.org/webgraphics.js"></script>
        <div>webgraphics script end</div>
        <script>
            async function renderAllWG() {
                let elems = document.getElementsByClassName('wg-div');
                for (let elem of elems) {
                    let id = elem.id;
                    let b64 = btoa(elem.getAttribute('data-wg'));
                    let dataUrl = 'data:application/json;base64,' + b64;
                    WG.Load(dataUrl, id);
                }
            }
        </script>
        <div>
            <button onclick="renderAllWG()">Click here to render all image using plantcyc's webgraphics library</button>
        </div>

        <style>
            td {
                border: 1px solid black;
            }
        </style>

        <table>
            <thead>
                <td>No.</td>
                <td>id</td>
                <td>name</td>
                <td>formula</td>
                <td>synonyms</td>
                <td>smiles</td>
                <td>inchi</td>
                <td>summary</td>
                <td>chebi</td>
                <td>kegg</td>
                <td>pubchem</td>
                <td>refmet</td>
                <td>image</td>
                <td>url</td>
            </thead>
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
    i = 0
    for id_ in data:
        i += 1
        tr = f'''<tr>
            <td>{i}</td>
            <td>{id_}</td>
            <td>{data[id_]["name"]}</td>
            <td>{data[id_]["formula"]}</td>
            <td>{data[id_]["synonyms"]}</td>
            <td>{data[id_]["smiles"]}</td>
            <td>{data[id_]["inchi"]}</td>
            <td>{data[id_]["summary"]}</td>
            <td>{data[id_]["chebi"]}</td>
            <td>{data[id_]["kegg"]}</td>
            <td>{data[id_]["pubchem"]}</td>
            <td>{data[id_]["refmet"]}</td>
            <td><div class='wg-div' id="wg-{id_}" data-wg="{escape(data[id_]["webgraphics_data"])}"></div></td>
            <td> <a href="{data[id_]["url"]}">{data[id_]["url"]}</a></td>
        </tr>'''
        trs.append(tr)
    tr_html = ''.join(trs)
    html = html_template % tr_html
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()

    
