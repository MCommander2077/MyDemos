import os
import gdown
import requests
from bs4 import BeautifulSoup

from django.http import HttpResponse, Http404, FileResponse, StreamingHttpResponse


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


def view(request):
    file_url = get_download_url(request.GET.get('url'))
    file_name = get_file_name(request.GET.get('url'))
    print(file_url, file_name)
    if not os.path.exists(f"./temp/{file_name}"):
        gdown.download(file_url)
    try:
        f = open(f"./temp/{file_name}", "rb")
        r = FileResponse(f, as_attachment=True, filename=file_name)
        return r
    except Exception:
        raise Http404("Download error")
