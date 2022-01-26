from blog.models import BlogPost, PostComment, Category
from rest_framework import serializers
from django.contrib.auth.models import User
from taggit.models import Tag
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


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
        
#XXX does not work
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('name',)
#         model = Tag


class PostSerializer(serializers.HyperlinkedModelSerializer):

    # 'author' needs to be set to PrimaryKeyRelatedField in order to be serialized.
    author = serializers.PrimaryKeyRelatedField(read_only=True,)

    # same.
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)   # XXX this way tags get displayed but can't be passed to create view
    # tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())     #XXX Does not work

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
        # representation["tags"] = TagSerializer(instance.tags).data        #XXX Does not work
        return representation


class PostCreateSerializer(PostSerializer):
    ''' Inherits parent in order to not allow 
        adding post views at creation time.'''
    class Meta(PostSerializer.Meta):
        fields = [
            'pk',
            'title',
            'title_image',
            'content',
            'author',
            'tags',
            'category',
        ]


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
        

class ResisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2',)


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "The password fields didn't match."})
        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )        
        user.set_password(validated_data['password'])
        user.save()
        return user