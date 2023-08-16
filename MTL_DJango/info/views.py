import requests
import json

from bs4 import BeautifulSoup
from django.shortcuts import render


def get_gdown_id(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    url = url.split('/')
    return url[5]


# Create your views here.

def view(request, song_id):
    data = requests.get(f'https://be.t21c.kro.kr/levels/{song_id}').text
    data = json.loads(data)
    data['gdownid'] = get_gdown_id(data['dlLink'])
    data['token'] = requests.get("https://cdn.mander.eu.org/api/get_key?password=M@nder_P^$$VV0RD][][").text
    return render(request, 'info.html', {'item': data})
