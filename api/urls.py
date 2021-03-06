from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'posts', views.PostViewSet)
# router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('posts/', views.PostListView.as_view()),
    path('comments/', views.CommentListView.as_view()),
    path('comment-create/', views.CommentCreateView.as_view()),
    path('comment-update/<int:pk>/', views.CommentUpdateDeleteView.as_view()),
    path('post-create/', views.PostCreateView.as_view()),
    path('post-update/<int:pk>/', views.PostUpdateDeleteView.as_view(), name='manufacturers'),
    path('register/', views.UserCreateView.as_view()),
    

]