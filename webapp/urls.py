from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("threads/show/<str:thread>", views.thread_show),
    path("login", views.sign_in, name="login"),
    path('logout', views.sign_out, name="logout"),
    path('add_group', views.add_group, name="add_group"),
    path('groups/', include([
        path('', views.group_index, name="group_index"),
        path('show/<int:groupID>', views.group_show , name="group_show"),
    ]))
]
