from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.blog_main, name='blog'),
    path('', views.PostListView.as_view(), name="blog"),
    path('post/<int:id>', views.post_detail, name='post_detail'),
    path('new', views.PostCreateView.as_view(), name='create_post'),
    path('edit/<int:pk>', views.PostEditView.as_view(), name='edit_post'),
    path('delete/<int:pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('comment/<int:pk>', views.add_comment, name='add_comment'),
    
]