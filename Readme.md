# Plantcyc Scraper
用于爬取[https://pmn.plantcyc.org/group?id=:ALL-COMPOUNDS&org-id=LER](https://pmn.plantcyc.org/group?id=:ALL-COMPOUNDS&org-id=LER)上的数据

## 如何使用
* 安装Python >= 3.7
* 设置python虚拟环境(venv)并激活
* 安装依赖软件包，在项目目录下运行`pip install -r requirements.txt`
* 网站右上角有 Export -> to spreadsheetfile -> 左下角frame IDs -> Export smarttable，然后把下载的文件第一行删掉，并命名为`PlantCyc_ids.txt`
* 运行命令`python plantcyc_scraper.py PlantCyc_ids.txt`开始爬取
* 脚本异常退出（如Ctrl-C或者网络问题）时会保存进度，保存到data.json，下载的网页保存在pages。再次运行可继续爬取。
* 运行命令`python data2html.py data.json out.html`生成网页out.html
* 打开out.html，复制所有内容到excel
