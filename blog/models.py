from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.expressions import F

# Create your models here.

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    title_image = models.ImageField(upload_to='posts/%d/%m/%Y')
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


class PostComment(models.Model):
    author = models.ForeignKey(User, related_name='comment_author', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, blank=False)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=500)

    

    def save(self, *args, **kwargs):
        if self.author is not None:
            if self.author.first_name and self.author.last_name:
                self.name = self.author.first_name + ' ' + self.author.last_name
            else:
                self.name = self.author.username

        super().save(*args, **kwargs)

    def __str__(self):
            return f"Comment {self.subject} by {self.name}"
