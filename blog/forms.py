from django import forms
from django.forms import ModelForm, widgets
from .models import BlogPost, PostComment

#not needed now.
class PostForm(ModelForm):
  model = BlogPost
  fields = ['title', 'title_image', 'content']


class CommentForm(ModelForm):
  class Meta:
    model = PostComment
    fields = ['name', 'author', 'email', 'subject', 'content']
    widgets = {'author': forms.HiddenInput()}