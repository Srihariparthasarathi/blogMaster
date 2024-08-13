from django.urls import path
from . import views

urlpatterns = [
    path('posts',views.Posts.as_view(), name='posts-list'),
    path('posts/<int:id>',views.IndividualPost.as_view(), name='induval-post'),
    
]
