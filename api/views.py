from blog.models import BlogPost, PostComment
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer

class PostList(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created')
    serializer_class = PostSerializer

class CommentList(generics.ListAPIView):
    queryset = PostComment.objects.all().order_by('-date_added')
    serializer_class = CommentSerializer


