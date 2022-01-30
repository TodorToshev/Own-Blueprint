from blog.models import BlogPost, PostComment
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import generics
from .serializers import CommentCreateSerializer, PostCreateSerializer, PostSerializer, CommentSerializer, ResisterSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created')
    serializer_class = PostSerializer

class CommentListView(generics.ListAPIView):
    queryset = PostComment.objects.all().order_by('-date_added')
    serializer_class = CommentSerializer

class CommentCreateView(generics.CreateAPIView):
    queryset = PostComment.objects.all().order_by('-date_added')
    serializer_class = CommentSerializer

class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostComment.objects.all()
    serializer_class = CommentCreateSerializer

class PostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all().order_by('-created')
    serializer_class = PostCreateSerializer

class PostUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all().order_by('-created')

    #not needed, QS automatically gets model instance.
    # def get_queryset(self):
    #     print("QS", self.request.parser_context['kwargs']['pk'])
    #     print("OO",self.request.query_params.get('pk'))
    #     return BlogPost.objects.filter(pk=self.request.parser_context['kwargs']['pk'])

    serializer_class = PostCreateSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, _ = Token.objects.get_or_create(user_id=response.data["id"])
        response.data["token"] = str(token)
        return response
