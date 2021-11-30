from django.shortcuts import render
from blog.models import BlogPost
from django.views.generic.list import ListView


# Create your views here.

def blog_main(request):
    return render(request, 'blog/blog.html')

class PostListView(ListView):

    model = BlogPost
    context_object_name = 'posts'
    template_name = 'blog/blog.html'
