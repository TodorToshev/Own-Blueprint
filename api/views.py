from blog.models import BlogPost, PostComment
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = BlogPost.objects.all().order_by('-created')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PostComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]