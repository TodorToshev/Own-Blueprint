from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.blog_main, name='blog'),
    path('', views.PostListView.as_view(), name="blog"),
]