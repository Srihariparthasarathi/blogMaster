from django.urls import path
from . import views

urlpatterns = [
    path('posts',views.Posts.as_view(), name='posts-list'),
    path('posts/<int:id>',views.IndividualPost.as_view(), name='induval-post'),
    path('comments',views.CommentPost.as_view(), name='comments'),
    path('comments/<int:id>',views.IndividualComment.as_view(), name='comment'),
    path('register',views.Register.as_view(), name='register'),
    path('login',views.LoginUser.as_view(), name='login'),
]
