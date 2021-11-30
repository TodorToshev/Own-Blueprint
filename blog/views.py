from django.shortcuts import render
from blog.models import BlogPost
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse



# def blog_main(request):
#     return render(request, 'blog/blog.html')

class PostListView(ListView):

    model = BlogPost
    context_object_name = 'posts'
    template_name = 'blog/blog.html'
    paginate_by = 10

def post_detail(request, id):
  post = get_object_or_404(BlogPost, id=id)
  return render(request, 'blog/post-details.html', {'post': post})


class PostCreateView(CreateView):
  model = BlogPost
  fields = ['title', 'content']
  template_name = 'blog/new.html'

  #get obj id and reverse to post/id
  def get_success_url(self):
    return reverse('blog:post_detail', args=(self.object.id,))

    
