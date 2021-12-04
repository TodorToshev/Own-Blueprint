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

    def get_context_data(self, **kwargs):
      context = super(PostListView, self).get_context_data(**kwargs)
      context['most_popular'] = BlogPost.objects.order_by('-views')[:5]
      return context

def post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    post.views += 1
    post.save()

    #repeating code, but otherwise the base.html gets messed up when I try to use inheritance.
    #TODO: fix 
    context = {
      'most_popular': BlogPost.objects.order_by('-views')[:5],
      'post': post
      }
    return render(request, 'blog/post-details.html', context)


class PostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'blog/new.html'

    #get obj id and reverse to post/id
    def get_success_url(self):
      return reverse('blog:post_detail', args=(self.object.id,))

    
