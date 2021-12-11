from django.contrib import admin
from .models import BlogPost, PostComment

# Register your models here.

# admin.site.register(BlogPost)
# admin.site.register(PostComment)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'tags', 'created', 'updated', 'views']

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'name', 'email', 'subject']

