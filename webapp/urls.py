from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login", views.sign_in, name="login"),
    path('register/', views.sign_up, name="register"),
    path('logout', views.sign_out, name="logout"),
    path('add_group', views.add_group, name="add_group"),
    path('groups/', include([
        path('', views.group_index, name="group_index"),
        path('show/<int:groupID>', views.group_show , name="group_show"),
        path('join/<int:groupID>', views.join_group, name="join_group"),
        path('edit/<int:groupID>', views.group_edit, name="group_edit"),
        path('delete/<int:groupID>', views.group_delete, name="group_delete")
    ])),
    path("threads/", include([
        path("show/<str:postID>", views.thread_show, name="thread_show"),
        path("comment/", include([
            path('reply<int:commentID>', views.reply_comment, name="reply_comment"),
            path('edit/<int:commentID>', views.comment_edit, name="comment_edit"),
            path('delete/<int:commentID>', views.comment_delete, name="comment_delete")
        ]))
    ])),
]
