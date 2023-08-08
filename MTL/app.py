import hashlib
import json
import os
import threading
import time

import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, Response, stream_with_context, render_template, request
from markupsafe import Markup as markup

static_sidebar_menu = f"""
<li><a href="../../"><span class="mif-home icon"></span>主页/Home</a></li>
        <li><a href="../../list"><span class="mif-books icon"></span>歌曲列表/List</a></li>
        <li class="divider"></li>
        <li><a href="../../about"><span class="mif-images icon"></span>关于这个项目/About This Project</a></li>
"""

# 定义全局变量
data = ''
data_num = 0

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = (os.urandom(24))



def get_file_name(url):
    if 'https://drive.google.com/' in url:
        res = requests.get(url)
        res.encoding = 'utf-8'
        url = url.split('/')
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.text.split('-')
        filename = title[0][0:(len(title[0])-1)]
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
        time.sleep(3600)


update_key = threading.Thread(target=main_loop)
update_key.setDaemon = True
update_key.start()


@app.route('/')
def index():
    return render_template('index.html', static_sidebar_menu=markup(static_sidebar_menu))


@app.route('/list')
def list():
    global data
    return render_template('list.html', data=data, static_sidebar_menu=markup(static_sidebar_menu))


@app.route('/admin')
def admin():
    return 'admin page is disabled'


@app.route('/about')
def about():
    return render_template('about.html', static_sidebar_menu=markup(static_sidebar_menu))


@app.route('/song/<int:song_id>', methods=['GET', 'POST'])
def get_song(song_id):
    if request.method == 'GET':
        res = json.loads(requests.get(f'https://be.t21c.kro.kr/levels/{song_id}').text)
        try:
            if res['statusCode']:
                return render_template('404.html', error=res['message'],
                                       static_sidebar_menu=markup(static_sidebar_menu)), 404  # 返回模板和状态码
        except:
            pass
        return render_template('info.html', item=res,
                               static_sidebar_menu=markup(static_sidebar_menu))


@app.route('/dl', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return ""
    file_name = get_file_name(url)
    if file_name:
        requests.get('https://cdn.mander.eu.org/api/dl_num/add?token=M@nder_P^$$VV0RD][][')
        # 发起HTTP GET请求获取文件
        response = requests.get(get_download_url(url), stream=True)
        #文件过大检测
        if 'Google 云端硬盘无法对此文件进行病毒扫描。' in response.text or 'Google Drive - Virus scan warning' in response.text:
            return f'''
            文件过大，为服务器着想暂不支持下载,或者您可以使用
            <a href="https://cdn.mander.eu.org/api/gdown?id={get_download_url(url).split('=')[-1]}&key={requests.get("https://cdn.mander.eu.org/api/get_key?password=M@nder_P^$$VV0RD][][").text}">ManderCDN</a>
            来进行下载
            '''

        # 设置响应头部信息，指定文件名和文件类型
        headers = {
            'Content-Disposition': f'attachment; filename={file_name}',
            'Content-Type': 'application/octet-stream'
        }

        # 创建响应对象
        return Response(
            stream_with_context(response.iter_content(chunk_size=1024)),
            headers=headers
        )
    else:
        return "下载失败或文件链接解析失败/Download Failed."


@app.route('/goto')
def goto():
    try:
        url = request.args.get('url')
    except Exception as e:
        return render_template('404.html', error=e, static_sidebar_menu=markup(static_sidebar_menu)), 404  # 返回模板和状态码
    if url:
        requests.get('https://cdn.mander.eu.org/api/dl_num/add?token=M@nder_P^$$VV0RD][][')
        return redirect(url, code=301)
    return ""


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', error=e, static_sidebar_menu=markup(static_sidebar_menu)), 404  # 返回模板和状态码


@app.errorhandler(500)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('500.html', error=e, static_sidebar_menu=markup(static_sidebar_menu)), 404  # 返回模板和状态码


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9812)
