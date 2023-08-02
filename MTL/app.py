import os
import threading
import time
import requests
import json
import gdown
import hashlib
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template, request, send_file

# 定义全局变量
data = ''
data_num = 0

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'secret_key')


def get_md5(str_input):
    md5 = hashlib.md5()
    md5.update(str(str_input).encode())
    return md5.hexdigest()


def remove_temp():
    temp_dir = './temp'
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))


def gd_dl(url):
    try:
        if 'https://drive.google.com/' in url:
            res = requests.get(url)
            res.encoding = 'utf-8'
            url = url.split('/')
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.title.text.split(' ')
            filename = title[0]
            if not os.path.exists(f"./temp/{filename}"):
                gdown.download(f"https://drive.google.com/uc?id={url[5]}", f"./temp/{filename}")
            return filename
        elif 'https://cdn.discordapp.com/' in url:
            res = requests.get(url)
            filename = url.split('/')[-1]
            if not os.path.exists(f"./temp/{filename}"):
                with open(f"./temp/{filename}", "wb") as f:
                    f.write(res.content)
            return filename
        else:
            return False
    except:
        return False


def get_21f_json():
    global data, data_num
    while True:
        try:
            all_data = json.loads(requests.get('https://be.t21c.kro.kr/levels').text)
            data = all_data['results']
        except Exception as error:
            pass
        else:
            return True


def main_loop():
    while 1:
        get_21f_json()
        remove_temp()
        app.config['SECRET_KEY'] = (os.urandom(24))
        # 配置WTF的CSRF，Value可以是任意的字符串
        app.config['WTF_CSRF_SECRET_KEY'] = (os.urandom(24))
        time.sleep(3600)


update_key = threading.Thread(target=main_loop)
update_key.setDaemon = True
update_key.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def list():
    global data
    return render_template('list.html', data=data)


@app.route('/admin')
def admin():
    return 'admin page is disabled'


@app.route('/song/<int:song_id>')
def get_song(song_id):
    res = json.loads(requests.get(f'https://be.t21c.kro.kr/levels/{song_id}').text)
    try:
        if res['statusCode']:
            return render_template('404.html', error=res['message']), 404  # 返回模板和状态码
    except:
        pass
    return render_template('info.html', item=res)


@app.route('/dl')
def download():
    try:
        url = request.args.get('url')
    except Exception as e:
        return render_template('404.html', error=e), 404  # 返回模板和状态码
    if url:
        file_name = gd_dl(url)
        if file_name:
            return send_file(f"./temp/{file_name}")
        else:
            return "下载失败或文件链接解析失败/Download Failed."
    else:
        return ""


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', error=e), 404  # 返回模板和状态码


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9812)
