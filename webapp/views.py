from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import *


# Create your views here.


def home(request):

    groups = Group.objects.order_by('created_at')
    posts = Post.objects.order_by('-created_at')    

    context = {
        'groupForm' : GroupForm(initial={'user': request.user}),
        'groups' : groups,
        'posts' : posts
    }
    
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'pages/about.html')




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


def sign_up(request):
    registerForm = RegistrationForm
    
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            return redirect(to="home")
        else:
            registerForm = RegistrationForm
    
    context = {
        'registerForm' : registerForm
    }
    return render(request, 'pages/register.html', context)

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
    
    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES)
        if postForm.is_valid():
            print('hello')
            postForm.save()
            return redirect(to="group_show", groupID=group.id)
        else:
            postForm = PostForm(initial={
                    'user' : request.user,
                    'group' : group
                    })
    
    context = {
        'group' : group,
        'postForm': postForm,
        'posts' : posts
    }
    
    return render(request, 'pages/groups/show.html', context)

@login_required(login_url='login')
@user_not_in_group
def join_group(request, groupID):
    group = Group.objects.get(id=groupID)
    group.users.add(request.user)
    group.save()
    return redirect(to="group_show", groupID=group.id)


@login_required(login_url='login')
@group_owner
def group_edit(request, groupID):
    group = Group.objects.get(id=groupID)
    groupForm = GroupForm(instance=group)
    
    if request.method == 'POST':
        groupForm = GroupForm(request.POST, request.FILES, instance=group)
        if groupForm.is_valid():
            groupForm.save()
            return redirect(to='group_show', groupID=group.id)
    
    context = {
        'group' : group,
        'groupForm' : groupForm
    }
    return render(request, 'pages/groups/edit.html', context)

@login_required(login_url='login')
@group_owner
def group_delete(request, groupID):
    group = Group.objects.get(id=groupID)
    group.delete()
    return redirect(to="group_index")



@login_required(login_url='login')
def thread_show(request, postID):
    post = Post.objects.get(id=postID)
    post_comments = Comment.objects.filter(post=post, reply__isnull=True).order_by('-created_at')

    commentForm = CommentForm(initial={'user' : request.user, 'post' : post})    
    if request.method == 'POST':
        commentForm = CommentForm(request.POST, initial={'user' : request.user, 'post' : post})
        if commentForm.is_valid():
            commentForm.save()
            return redirect(to="thread_show", postID=post.id)
    
    context = {
        'post' : post,
        'commentForm' : commentForm,
        'post_comments' : post_comments
    }
    return render(request, 'pages/threads/show.html', context)


def thread_delete(request, postID):
    post = Post.objects.get(id=postID)
    post.delete()
    return redirect(to="group_show", groupID=post.group.id)


@login_required(login_url='login')
def thread_edit(request, postID):
    post = Post.objects.get(id=postID)
    postForm  = PostForm(instance=post)

    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES, instance=post)
        if postForm.is_valid():
            postForm.save()
            return redirect(to="thread_show", postID=post.id)
        
    context = {
        'post' : post,
        'postForm' : postForm
    }
    
    
    return render(request, 'pages/threads/edit.html', context)


@login_required(login_url='login')
def comment_edit(request, commentID):
    comment = Comment.objects.get(id=commentID)
    commentForm = CommentForm(request.POST, instance=comment)
    commentForm.save()
    return redirect(to="thread_show", postID=comment.post.id)

@login_required(login_url='login')
def comment_delete(request, commentID):
    comment = Comment.objects.get(id=commentID)
    comment.delete()
    return redirect(to="thread_show", postID=comment.post.id)

@login_required(login_url="login")
def reply_comment(request, commentID):
    parent_comment = Comment.objects.get(id=commentID)

    if request.method == 'POST':
        reply_form = CommentForm(request.POST)
        if reply_form.is_valid():
            reply_comment = reply_form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.post = parent_comment.post
            reply_comment.reply = parent_comment  # Associate the reply with the parent comment
            reply_comment.save()

            return redirect('thread_show', postID=parent_comment.post.id)

    return redirect('thread_show', postID=parent_comment.post.id)
    

@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect(to="home")