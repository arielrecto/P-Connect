from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):

    groups = Group.objects.order_by('created_at')    

    context = {
        'groupForm' : GroupForm(initial={'user': request.user}),
        'groups' : groups
    }
    
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'pages/about.html')

def thread_show(request, thread):
    return render(request, 'pages/threads/show.html')


def sign_in(request):
    if request.method == 'POST':
        credentialsData = {
            'username' : request.POST.get('username'),
            'password' : request.POST.get('password')
        }
        
        authenticated_user = authenticate(username=credentialsData['username'], password=credentialsData['password'])
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect(to='home')
        return redirect(to='login')
        
     
    
    context = {
        'loginForm' : LoginForm
    }
    
    
    return render(request, 'pages/login.html', context)

@login_required(login_url='login')
def add_group(request):
    groupForm = GroupForm(request.POST, request.FILES, initial={'user': request.user})
    if groupForm.is_valid():
        groupForm.save()
        return redirect(to="home")
    return render(request, 'home.html', {'groupForm' : groupForm})


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect(to="home")