from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    msg = 'Here you can collate your datasets'
    return HttpResponse(msg)
