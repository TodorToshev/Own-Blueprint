from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.blog_main, name='blog'),
    # path('', views.PostListView.as_view(), name="blog"),
    path('', views.post_list, name="blog"),
    path('tag/<slug:tag_slug>/', views.post_list, name="list_by_tag"),
    path('category/<int:pk>/', views.post_list, name="list_by_categ"),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('new/', views.PostCreateView.as_view(), name='create_post'),
    path('edit/<int:pk>/', views.PostEditView.as_view(), name='edit_post'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete_post'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('search/', views.basic_search, name='search'),
    
]