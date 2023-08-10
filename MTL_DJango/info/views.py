import requests
import json
from django.shortcuts import render


# Create your views here.

def view(request, song_id):
    data = requests.get(f'https://be.t21c.kro.kr/levels/{song_id}').text
    data = json.loads(data)
    print(data)
    return render(request, 'info.html',{'item':data})
