from django import forms
from .models import *



class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': 'input input-accent bg-gray-100', 'placeholder': 'username'}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'class': 'input input-accent bg-gray-100', 'placeholder': 'password'}))

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'image',
            'name',
            'description',
            'owner',
            'category'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-accent bg-gray-100'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-accent bg-gray-100'}),
            'category': forms.SelectMultiple(attrs={'class': 'select select-accent bg-gray-100'}),
            'image': forms.FileInput(attrs={'class': 'file-input file-input-accent bg-gray-100'}),
            'owner': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        """
        The `__init__` function initializes a form and sets the initial value of the 'owner' field to
        the value of the 'user' field if it exists in the initial data.
        """
        super(GroupForm, self).__init__(*args, **kwargs)

        if 'user' in self.initial:
            self.initial['owner'] = self.initial['user']
            

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'input input-accent input-sm bg-gray-100', 'placeholder' : 'Title'}),
            'content' : forms.Textarea(attrs={'class' : 'textarea textarea-accent bg-gray-100 h-20', 'placeholder' : 'Content'}),
            'image' : forms.FileInput(attrs={'class' : 'file-input file-input-accent bg-gray-100'}),
            'user' : forms.HiddenInput(),
            'group' : forms.HiddenInput()
        }