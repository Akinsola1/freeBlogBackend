from django.urls import path, include
from . import views
urlpatterns = [
    path('signup', views.signupuser),
    path('login', views.login_user),
    path('create-post',views.createPost ),
    path('get-my-post', views.getMyPost),
    path('get-all-post', views.getAllPost),
    path('like-a-post',views.likeAPost),
    path('comment-on-post',views.commentOnPost),
    path('get-post-comment/<str:id>',views.getPostComment),
]
