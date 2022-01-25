from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
# router.register(r'posts', views.PostViewSet)
# router.register(r'comments', views.CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('posts/', views.PostListView.as_view()),
    path('comments/', views.CommentListView.as_view()),
    path('comment-create/', views.CommentCreateView.as_view()),

]