from django.forms import ModelForm
from .models import BlogPost
#not needed now.
class PostForm(ModelForm):
  model = BlogPost
  fields = ['title', 'title_image', 'content']
