from blog.models import BlogPost, PostComment, Category
from rest_framework import serializers
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username')
        model = User

class CommentRelatedPostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title')
        model = BlogPost


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('categ_type',)
        model = Category

class PostSerializer(serializers.HyperlinkedModelSerializer):
    # 'author' needs to be set to PrimaryKeyRelatedField in order to be serialized.
    author = serializers.PrimaryKeyRelatedField(read_only=True,)

    # same.
    category = serializers.PrimaryKeyRelatedField(read_only=True,)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'pk',
            'title',
            'title_image',
            'content',
            'created',
            'updated',
            'author',
            'views',
            'tags',
            'category',
        ]

    def to_representation(self, instance):
        ''' Overriding in order to display not only ids, but also names of author and category.
        Author and Category serializers are defined abovewith the corresponding category and 
        the fields we want to be serialized. '''
        representation = super().to_representation(instance)
        
        # here, 'instance' is the blog post to be serialized and 'author' and 'category' - 
        # the fields to be serialized.
        representation["author"] = AuthorSerializer(instance.author).data
        representation["category"] = CategorySerializer(instance.category).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True,)
    post = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all())

    class Meta:
        model = PostComment
        fields = [
            'author',
            'post',
            'name',
            'email',
            'subject',
            'content',
            'date_added',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = AuthorSerializer(instance.author).data
        
        # references CommentRelatedPostSerializer to display only two 
        # fields instead of the main post serializer.
        representation["post"] = CommentRelatedPostSerializer(instance.post).data
        return representation
        