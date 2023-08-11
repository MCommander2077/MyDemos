import os
import json

from django.shortcuts import render


# Create your views here.

def view(request):
    with open('./data.txt', 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    data = json.loads(data)
    data = data['results']
    return render(request, 'list.html', {'data': data})
