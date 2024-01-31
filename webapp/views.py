from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import *


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
def group_index(request):
    groups = Group.objects.order_by('created_at')
    context = {
        'groups' : groups
    }
    
    return render(request, 'pages/groups/index.html', context)

@login_required(login_url='login')
@group_required
def group_show(request, groupID):
    group = Group.objects.get(id=groupID)
    posts = Post.objects.filter(group=group).order_by('-created_at')
    

    
    postForm = PostForm(initial={
        'user' : request.user,
        'group' : group
    })
    context = {
        'group' : group,
        'postForm': postForm,
        'posts' : posts
    }
    
    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES)
        if postForm.is_valid():
            postForm.save()
            return redirect(to="group_show", groupID=group.id)
        
        context = {
        'group' : group,
        'postForm': postForm,
        'posts' : posts
        }
    
        return render(request, 'pages/groups/show.html', context)
    
    return render(request, 'pages/groups/show.html', context)

@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect(to="home")