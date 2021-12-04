from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    # content = models.TextField()
    content = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='post_author', on_delete=models.SET_NULL, null=True)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title