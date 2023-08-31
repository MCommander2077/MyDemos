# --------------THE KEY-----------------
CDN_KEY = 'M@nder_P^$$VV0RD][]['
# --------------THE KEY-----------------

import hashlib
import random
import gdown
import requests
from bs4 import BeautifulSoup
from flask import Flask, send_file, request, Response, stream_with_context

with open('dldata.txt', 'r') as f:
    dl_num = int(f.readlines()[0])
    f.close()


def get_file_name(url):
    if 'https://drive.google.com/' in url:
        res = requests.get(url)
        res.encoding = 'utf-8'
        url = url.split('/')
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.text.split('-')
        filename = title[0][0:(len(title[0]) - 1)]
        return filename
    elif 'https://cdn.discordapp.com/' in url:
        res = requests.get(url)
        filename = url.split('/')[-1]
        return filename


def get_download_url(url):
    try:
        if 'https://drive.google.com/' in url:
            res = requests.get(url)
            res.encoding = 'utf-8'
            url = url.split('/')
            return f"https://drive.google.com/uc?export=download&id={url[5]}"
        elif 'https://cdn.discordapp.com/' in url:
            return url
        else:
            return url
    except:
        return False


def get_md5(str_input):
    md5 = hashlib.md5()
    md5.update(str(str_input).encode())
    return md5.hexdigest()


apikeys = []

app = Flask(__name__)


@app.route('/')
def index():
    return f""


@app.route('/api/get_key')
def api_get_key():
    password = request.args['password']

    if CDN_KEY == password:
        add_key = str(
            get_md5(
                random.random()
            )
        )
        apikeys.append(
            add_key
        )
        return add_key
    return f"key error"


@app.route('/api/dl_num/get')
def get_dl_num():
    global dl_num
    token = request.args['token']
    if token == CDN_KEY:
        return str(dl_num)
    return ""


@app.route('/api/dl_num/add')
def add_dl_num():
    global dl_num
    token = request.args['token']
    if token == CDN_KEY:
        dl_num = dl_num + 1
        with open('dldata.txt', 'w') as f:
            f.write(str(dl_num))
            f.close()
        return "True"
    return ""


@app.route('/api/get_file/<name>/<file>')
def get_file(name, file):
    try:
        key = request.args['key']
    except:
        return f"please input key"
    if not key in apikeys:
        return f"key error"
    apikeys.remove(key)
    try:
        return send_file(f'{name}\\{file}')
    except Exception as error:
        return f"{error}"


@app.route('/api/download')
def download_file():
    global dl_num
    key = request.args['key']
    url = request.args['url']
    if not key:
        return "key?"
    if not key in apikeys:
        return "wrong key"
    apikeys.remove(key)
    url = request.args.get('url')
    if not url:
        return ""
    file_name = get_file_name(url)
    file_url = get_download_url(url)
    if file_name:
        requests.get('https://cdn.mander.eu.org/api/dl_num/add?token=M@nder_P^$$VV0RD][][')
        # 发起HTTP GET请求获取文件
        response = requests.get(file_url, stream=True)
        # 文件过大检测
        if 'Google 云端硬盘无法对此文件进行病毒扫描。' in response.text or 'Google Drive - Virus scan warning' in response.text:
            gdown.download(file_url, f"./temp/{file_name}")
            dl_num = dl_num + 1
            with open('dldata.txt', 'w') as f:
                f.write(str(dl_num))
                f.close()
            return send_file(f"./temp/{file_name}")

        # 设置响应头部信息，指定文件名和文件类型
        headers = {
            'Content-Disposition': f'attachment; filename={file_name}',
            'Content-Type': 'application/octet-stream'
        }
        dl_num = dl_num + 1
        with open('dldata.txt', 'w') as f:
            f.write(str(dl_num))
            f.close()
        # 创建响应对象
        return Response(
            stream_with_context(response.iter_content(chunk_size=1024)),
            headers=headers
        )
    else:
        return "下载失败或文件链接解析失败/Download Failed."


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return "404 Not Found"


@app.errorhandler(400)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return "Need arg(s) Not Found"


@app.errorhandler(500)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return "Server Error,Please Send E-mail to me@mcommander.eu.org"


if __name__ == '__main__':
    app.run(port=5001)
