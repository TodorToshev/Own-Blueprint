from django.shortcuts import redirect, render
from blog.models import BlogPost, PostComment
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import CommentForm
from django.contrib import messages
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category


# def blog_main(request):
#     return render(request, 'blog/blog.html')

# class PostListView(ListView):

#     model = BlogPost
#     context_object_name = 'posts'
#     template_name = 'blog/blog.html'
#     paginate_by = 10

#     def get_context_data(self, **kwargs):
#       context = super(PostListView, self).get_context_data(**kwargs)
#       context['most_popular'] = BlogPost.objects.order_by('-views')[:5]
#       return context


def post_list(request, tag_slug=None):
    tag = None
    posts = BlogPost.objects.all()
    
    if tag_slug:
      tag = get_object_or_404(Tag, slug=tag_slug)
      posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
      posts = paginator.page(page)
    except PageNotAnInteger:
      # If page is not an integer deliver the first page
      posts = paginator.page(1)
    except EmptyPage:
      # If page is out of range deliver last page of results
      posts = paginator.page(paginator.num_pages)

    context = {
      'most_popular': BlogPost.objects.order_by('-views')[:5],
      'posts': posts,
      'page': posts,
      'tags': Tag.objects.all(),
      'categories': Category.objects.all(),
    }

    return render(request, 'blog/blog.html', context)

def post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    post.views += 1
    post.save()

    comment_form = CommentForm()
    post_comments = PostComment.objects.filter(post__id=id)

    #repeating code, but otherwise the base.html gets messed up when I try to use inheritance.
    #TODO: fix 
    context = {
      'most_popular': BlogPost.objects.order_by('-views')[:5],
      'post': post,
      'comment_form': comment_form,
      'post_comments': post_comments,
      'tags': Tag.objects.all(),
      'categories': Category.objects.all(),
      }
    return render(request, 'blog/post-details.html', context)


def add_comment(request, pk):
  post = get_object_or_404(BlogPost, id=pk)
  comment_form = CommentForm()
  if request.method == 'POST':
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      try:
        comment.author = request.user
      except ValueError:
        comment.author = None
      comment.post = post
      comment.save()
      messages.success(request, 'Comment has been posted.')  
  
  return redirect('blog:post_detail', post.id)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'category', 'title_image', 'content', 'tags']
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
    fields = ['title', 'category', 'title_image', 'content', 'tags']
    template_name = 'blog/edit.html'

    def get_context_data(self, **kwargs):
      context = super(PostEditView, self).get_context_data(**kwargs)
      context['post'] = self.object
      return context

    def dispatch(self, request, *args, **kwargs):
      post = self.get_object()
      if not (request.user == post.author or request.user.is_superuser):
          return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
      return reverse('blog:post_detail', args=(self.object.id,))


class PostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:blog')
    template_name = 'blog/delete.html'
    

def basic_search(request):
    if request.method == 'POST':
      term = request.POST.get('term', default=False)
      results = BlogPost.objects.filter(title__icontains=term) | \
          BlogPost.objects.filter(content__icontains=term)
      context = {'results': results,
                 'term': term,
                 'tags': Tag.objects.all(), }
      return render(request, 'blog/search_result.html', context)
    else:
      return render(request, 'blog/search_result.html')
