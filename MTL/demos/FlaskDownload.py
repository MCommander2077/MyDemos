from bs4 import BeautifulSoup
from flask import Flask, Response, stream_with_context
import requests

app = Flask(__name__)



@app.route('/')
def index():
    url = 'https://cdn.discordapp.com/attachments/674252951124181012/878863361901756496/Nisemono.zip'  # 替换为要下载的文件链接

    # 获取文件的大小和文件名
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length'))
    file_name = 'Nisemono.zip'  # 可以根据需要修改文件名

    # 设置响应头，指定下载文件的类型和文件名
    headers = {
        'Content-Disposition': f'attachment; filename="{file_name}"',
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(file_size)
    }

    # 发送响应头
    def generate():
        yield b' ' * 8192  # 预留一些空间，防止浏览器提前关闭连接
        yield b'\n'

        # 下载文件并逐步发送给客户端
        with requests.get(url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    return Response(generate(), headers=headers, direct_passthrough=True)

@app.route('/download', methods=['GET'])
def download_file():
    url = 'https://cdn.discordapp.com/attachments/674252951124181012/878863361901756496/Nisemono.zip'  # 替换为实际文件的 URL

    # 发起HTTP GET请求获取文件
    response = requests.get(url, stream=True)

    # 设置响应头部信息，指定文件名和文件类型
    headers = {
        'Content-Disposition': 'attachment; filename=Nisemono.zip',
        'Content-Type': 'application/octet-stream'
    }

    # 创建响应对象
    return Response(
        stream_with_context(response.iter_content(chunk_size=1024)),
        headers=headers
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
