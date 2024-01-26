from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    
    Gender = (
       ('M', 'Male'),
       ('F', 'Female')
    )
    
    last_name = models.CharField(max_length=55)
    first_name = models.CharField(max_length=55)
    middle_name = models.CharField(max_length=55, blank=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=1, choices=Gender)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.last_name
    
class Category(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    
class Group (models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    owner = models.ForeignKey(User, db_column="owner_id", related_name="owner", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)
    media = models.FileField(upload_to="post_media", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content
    
class Vote(models.Model):
     name = models.CharField(max_length=55)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     post = models.ForeignKey(Post, on_delete=models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
     def __str__(self):
        return self.name