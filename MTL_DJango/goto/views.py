import requests
from django.http import HttpResponse
from django.shortcuts import render,redirect


# Create your views here.

def view(request):
    try:
        url = request.GET.get('url')
        requests.get('https://cdn.mander.eu.org/api/dl_num/add?token=M@nder_P^$$VV0RD][][')
        return redirect()
    except:
        return HttpResponse("Error")