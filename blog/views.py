from django.shortcuts import render
from blog.models import BlogPost
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'blog/new.html'

    def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.author = self.request.user
      self.object.save()
      return super().form_valid(form)

    #get obj id and reverse to post/id
    def get_success_url(self):
      return reverse('blog:post_detail', args=(self.object.id,))

    
class PostEditView(LoginRequiredMixin, UpdateView):
  model = BlogPost
  fields = ['title', 'content']
  template_name = 'blog/edit.html'

  def dispatch(self, request, *args, **kwargs):
    post = self.get_object()
    if not (request.user == post.author or request.user.is_superuser):
        return self.handle_no_permission()
    return super().dispatch(request, *args, **kwargs)

  def get_success_url(self):
    return reverse('blog:post_detail', args=(self.object.id,))

