from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'pages/about.html')

def thread_show(request, thread):
    return render(request, 'pages/threads/show.html')