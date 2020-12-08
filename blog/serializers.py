from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username']


class PostListSerializer(serializers.ModelSerializer):
  category = CategorySerializer()
  author = UserSerializer()

  class Meta:
    model = Post
    fields = ['id', 'title', 'created_time', 'excerpt', 'category', 'author', 'views']


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name']


class PostRetrieveSerializer(serializers.ModelSerializer):
  category = CategorySerializer()
  tags = TagSerializer(many=True)
  author = UserSerializer()
  toc = serializers.CharField(label='文章目录', help_text='HTML 格式，每个目录条目均由 li 标签包裹。')
  body_html = serializers.CharField(label='文章内容', help_text='HTML 格式， 从 `body` 字段解析而来')

  class Meta:
    model = Post
    fields = ['id', 'title', 'body', 'created_time', 'modified_time', 'excerpt', 'views', 'category', 'author', 'tags', 'toc', 'body_html']
