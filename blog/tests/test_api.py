from datetime import datetime

from django.utils.timezone import utc
from django.core.cache import cache
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from blog.models import Category, Post, Tag
from comments.models import Comment
from blog.serializers import (
  CategorySerializer,
  PostListSerializer,
  PostRetrieveSerializer,
  TagSerializer
)
from comments.serializers import CommentSerializer


class PostViewSetTestCase(APITestCase):
  def setUp(self):
    cache.clear()  # 清除缓存，防止限流
    user = User.objects.create_superuser(username='admin', email='admin@qq.com', password='admin')
    self.cate1 = Category.objects.create(name='category 1')
    self.cate2 = Category.objects.create(name='category 2')
    self.tag1 = Tag.objects.create(name='tag1')
    self.tag2 = Tag.objects.create(name='tag2')
    self.post1 =  Post.objects.create(title='title 1', body='post 1', category=self.cate1, author=user,created_time=datetime(year=2020, month=7, day=10).replace(tzinfo=utc))
    self.post1.tags.add(self.tag1)
    self.post2 =  Post.objects.create(title='title 2', body='post 2', category=self.cate1, author=user,created_time=datetime(year=2020, month=7, day=31).replace(tzinfo=utc))
    self.post2.tags.add(self.tag1)
    self.post3 =  Post.objects.create(title='title 3', body='post 3', category=self.cate2, author=user,created_time=datetime(year=2020, month=8, day=1).replace(tzinfo=utc))
    self.post3.tags.add(self.tag2)
    self.comment1 = Comment.objects.create(name='u1', email='u1@qq.com', text='comment 1', post=self.post3)
    self.comment2 = Comment.objects.create(name='u2', email='u2@qq.com', text='comment 2', post=self.post3)

  def test_list_post(self):
    """
    测试文章列表接口
    """
    url = reverse('v1:post-list')  # 获取文章列表接口的URL
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = PostListSerializer(instance=[self.post3, self.post2, self.post1], many=True)
    self.assertEqual(response.data['results'], serializer.data)

  def test_list_post_filter_by_category(self):
    """
    测试某个分类下的文章列表接口
    """
    url = reverse('v1:post-list')
    response = self.client.get(url, {'category': self.cate1.pk})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = PostListSerializer(instance=[self.post2, self.post1], many=True)
    self.assertEqual(response.data['results'], serializer.data)

  def test_list_post_filter_by_tag(self):
    """
    测试某个标签下的文章列表接口
    """
    url = reverse('v1:post-list')
    response = self.client.get(url, {'tags': self.tag1.pk})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = PostListSerializer(instance=[self.post2, self.post1], many=True)
    self.assertEqual(response.data['results'], serializer.data)

  def test_list_post_filter_by_archive_date(self):
    """
    测试某个归档日期下的文章列表接口
    """
    url = reverse('v1:post-list')
    response = self.client.get(url, {'created_year': 2020, 'created_month': 7})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = PostListSerializer(instance=[self.post2, self.post1], many=True)
    self.assertEqual(response.data['results'], serializer.data)

  def test_retrieve_post(self):
    """
    测试单篇文章详情接口
    """
    url = reverse('v1:post-detail', kwargs={'pk': self.post1.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = PostRetrieveSerializer(instance=self.post1)
    self.assertEqual(response.data, serializer.data)

  def test_retrieve_inexistent_post(self):
    """
    获取一篇不存在的文章
    """
    url = reverse('v1:post-detail', kwargs={'pk': 999})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_list_archive_dates(self):
    """
    测试获取文章归档日期列表接口
    """
    url = reverse('v1:post-archive-date')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, ['2020-08', '2020-07'])

  def test_list_comments(self):
    """
    测试某篇文章的评论列表接口
    """
    url = reverse('v1:post-comment', kwargs={'pk': self.post3.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = CommentSerializer(instance=[self.comment2, self.comment1], many=True)
    self.assertEqual(response.data['results'], serializer.data)

  def test_list_inexistent_post_comments(self):
    """
    测试某篇不存在的文章的评论列表
    """
    url = reverse('v1:post-comment', kwargs={'pk': 999})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryViewSetTestCase(APITestCase):
  def setUp(self):
    self.cate1 = Category.objects.create(name='category 1')
    self.cate2 = Category.objects.create(name='category 2')
  
  def test_list_categories(self):
    url = reverse('v1:category-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = CategorySerializer(instance=[self.cate1, self.cate2], many=True)
    self.assertEqual(response.data, serializer.data)
  
class TagViewSetTestCase(APITestCase):
  def setUp(self):
    self.tag1 = Tag.objects.create(name='tag1')
    self.tag2 = Tag.objects.create(name='tag2')
  
  def test_list_tags(self):
    url = reverse('v1:tag-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = TagSerializer(instance=[self.tag1, self.tag2], many=True)
    self.assertEqual(response.data, serializer.data)
