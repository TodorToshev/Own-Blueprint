from django import forms
from django.forms import ModelForm, widgets
from .models import BlogPost, PostComment

#not needed now.
# class PostForm(ModelForm):
#   model = BlogPost
#   fields = ['title', 'title_image', 'content', 'tags']


class CommentForm(ModelForm):
  class Meta:
    model = PostComment
    fields = ['name', 'email', 'subject', 'content']
    widgets = {'name': widgets.TextInput(attrs={
                   'placeholder': 'name (user name will be displayed if logged in)'}),
               'email': widgets.TextInput(attrs={
                   "placeholder": 'email'}),
               # 'content': widgets.TextInput(attrs={
               #   "placeholder": 'comment'}),
               'subject': widgets.TextInput(attrs={
                   "placeholder": 'subject'}),

               }
