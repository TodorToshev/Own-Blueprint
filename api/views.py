from blog.models import BlogPost, PostComment
from rest_framework import permissions
from rest_framework import generics
from .serializers import CommentCreateSerializer, PostCreateSerializer, PostSerializer, CommentSerializer, ResisterSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in self.SAFE_METHODS or
            obj.author == request.user
        )


class PostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created')
    serializer_class = PostSerializer


class CommentListView(generics.ListAPIView):
    queryset = PostComment.objects.all().order_by('-date_added')
    serializer_class = CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    queryset = PostComment.objects.all().order_by('-date_added')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostComment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all().order_by('-created')
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]


class PostUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all().order_by('-created')

    #not needed, QS automatically gets model instance.
    # def get_queryset(self):
    #     print("QS", self.request.parser_context['kwargs']['pk'])
    #     print("OO",self.request.query_params.get('pk'))
    #     return BlogPost.objects.filter(pk=self.request.parser_context['kwargs']['pk'])

    serializer_class = PostCreateSerializer

    permission_classes = [IsOwnerOrReadOnly]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, _ = Token.objects.get_or_create(user_id=response.data["id"])
        response.data["token"] = str(token)
        return response
