from blog.models import BlogPost, PostComment
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer

class PostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created')
    serializer_class = PostSerializer

class CommentListView(generics.ListAPIView):
    queryset = PostComment.objects.all().order_by('-date_added')
    serializer_class = CommentSerializer

class CommentCreateView(generics.CreateAPIView):
    queryset = PostComment.objects.all().order_by('-date_added')
    serializer_class = CommentSerializer
