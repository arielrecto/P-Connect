from django.contrib import admin
from webapp.models import (Post, Group, Vote, Comment, Category, Profile)

# Register your models here.


admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Profile)