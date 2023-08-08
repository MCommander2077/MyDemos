import requests
from bs4 import BeautifulSoup

#--------------THE KEY-----------------
CDN_KEY = ''
#--------------THE KEY-----------------

from flask import Flask, send_file, request
import gdown
import random
import hashlib
import threading

with open('dldata.txt', 'r') as f:
    dl_num = int(f.readlines()[0])
    f.close()

def get_file_name(url):
        res = requests.get(url)
        res.encoding = 'utf-8'
        url = url.split('/')
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.text.split(' ')
        filename = title[0]
        return filename


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
            f.write(dl_num)
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

@app.route('/api/gdown')
def gdown_file():
    key = request.args['key']
    gd_id = request.args['id']
    file_name = get_file_name(f"https://drive.google.com/file/d/{gd_id}/view")
    if not key:
        return "key?"
    if not key in apikeys:
        return "wrong key"
    apikeys.remove(key)
    try:
        threading.Thread(target=gdown.download,args=(f"https://drive.google.com/uc?export=download&id={gd_id}",f'./temps/{file_name}')).start()
    except Exception as error:
        print(f"{error}")
        return f"error"

    return send_file(f'temps/{file_name}')

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
