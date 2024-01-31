from functools import wraps
from django.shortcuts import render, HttpResponse, redirect
from .models import *  # Make sure to import your Group model

def group_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
     
        user = request.user
        group_id = kwargs.get('groupID')

      
        group = Group.objects.filter(id=group_id).first()

        if user.is_authenticated and group.users.filter(id=user.id).exists() or group.owner.id == user.id:
            return view_func(request, *args, **kwargs)
        else:
            if not user.is_authenticated:
                return redirect(to='login')
            else:
                return redirect(to="group_index")
            

    return wrapper


def user_not_in_group(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        group_id = kwargs.get('groupID')
        user = request.user

        if user.is_authenticated:
            group = Group.objects.get(id=group_id)

            # Check if the user is already in the group
            if user in group.users.all():
                # User is already in the group, redirect back or return a response
                return redirect('group_index')

        # User is not in the group, proceed with the view
        return view_func(request, *args, **kwargs)

    return wrapper