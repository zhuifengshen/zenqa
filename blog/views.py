import re
import markdown
from markdown.extensions.toc import TocExtension

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.db.models.aggregates import Count

from .models import Post, Category, Tag
from pure_pagination import PaginationMixin

from rest_framework.decorators import api_view, action
from rest_framework.serializers import DateField
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.throttling import AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from .serializers import CategorySerializer, UserSerializer, PostListSerializer, PostRetrieveSerializer, TagSerializer
from comments.serializers import CommentSerializer
from .filters import PostFilter


"""
# Create your views here.
def index(request):
  # return HttpResponse('欢迎访问我的博客首页！')
  # return render(request, 'blog/index.html', context={
  #   'title': '我的博客首页',
  #   'welcome': '欢迎访问我的博客首页！'
  # })
  post_list = Post.objects.all()
  return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
  cate = get_object_or_404(Category, pk=pk)
  # post_list = Post.objects.filter(category=cate)
  post_list = cate.post_set.all()
  return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request, pk):
  tag = get_object_or_404(Tag, pk=pk)
  post_list = Post.objects.filter(tags=tag)
  return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.increase_views()  # 阅读量 +1

  # post.body = markdown.markdown(post.body, extensions=[
  #   'markdown.extensions.extra',
  #   'markdown.extensions.codehilite',
  #   'markdown.extensions.toc',
  # ])
  md = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    # 'markdown.extensions.toc',
    TocExtension(slugify=slugify),
  ])
  post.body = md.convert(post.body)

  m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
  post.toc = m.group(1) if m is not None else ''

  return render(request, 'blog/detail.html', context={'post': post})
"""


def archive(request, year, month):
  post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
  return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(PaginationMixin, ListView):
  model = Post
  template_name = 'blog/index.html'
  context_object_name = 'post_list'
  paginate_by = 10  # 指定每页包含文章数


# class CategoryView(ListView):
#   model = Post
#   template_name = 'blog/index.html'
#   context_object_name = 'post_list'
#   def get_queryset(self):
#     cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#       return super(CategoryView, self).get_queryset().filter(category=cate)


class CategoryView(IndexView):
  def get_queryset(self):
    cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
    return super(CategoryView, self).get_queryset().filter(category=cate)
  

class TagView(IndexView):
  def get_queryset(self):
    tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
    return super(TagView, self).get_queryset().filter(tags=tag)


class PostDetailView(DetailView):
  model = Post
  template_name = 'blog/detail.html'
  context_object_name = 'post'

  def get(self, request, *args, **kwargs):
    """阅读量 +1"""
    response = super(PostDetailView, self).get(request, *args, **kwargs)
    self.object.increase_views()
    return response
  
  # def get_object(self, queryset=None):
  #   """文章内容处理"""
  #   post = super().get_object(queryset=None)
  #   md = markdown.Markdown(extensions=[
  #     'markdown.extensions.extra',
  #     'markdown.extensions.codehilite',
  #     # 'markdown.extensions.toc',
  #     TocExtension(slugify=slugify),
  #   ])
  #   post.body = md.convert(post.body)
  #   m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
  #   post.toc = m.group(1) if m is not None else ''    
  #   return post

  
def search(request):
  q = request.GET.get('q')

  if not q:
    error_msg = "请输入搜索关键词"
    messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
    return redirect('blog:index')
  
  post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))  # Q对象用于包装查询表达式，提供复杂的查询逻辑
  return render(request, 'blog/index.html', {'post_list': post_list})


def about(request):
  return render(request, 'blog/about.html')




# ---------------------------------------------------------------------------
#   Django REST framework 接口
# ---------------------------------------------------------------------------


class TagAnonRateThrottle(AnonRateThrottle):
  THROTTLE_RATES = {'anon': '5/min'}


# @api_view(http_method_names=['GET'])
# def index(request):
#   post_list = Post.objects.all()
#   serializer = PostListSerializer(post_list, many=True)
#   return Response(serializer.data, status=status.HTTP_200_OK)

class IndexPostListAPIView(ListAPIView):
  serializer_class = PostListSerializer
  queryset = Post.objects.all()
  pagination_class = PageNumberPagination
  permission_classes = [AllowAny]


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  博客文章视图集

  list:
  返回博客文章列表

  retrieve:
  返回博客文章详情

  list_comments:
  返回博客文章下的评论列表

  list_archive_dates:
  返回博客文章归档日期列表
  """
  serializer_class = PostListSerializer
  queryset = Post.objects.all()
  pagination_class = LimitOffsetPagination
  permission_classes = [AllowAny]
  filter_backends = [DjangoFilterBackend]
  filterset_class = PostFilter

  serializer_class_table = {
    'list': PostListSerializer,
    'retrieve': PostRetrieveSerializer,
  }

  def get_serializer_class(self):
    return self.serializer_class_table.get(self.action, super().get_serializer_class())
  
  @swagger_auto_schema(responses={200: '归档日期列表，时间倒序排列。例如：["2020-08", "2020-06"]'})
  @action(
    methods=['GET'],
    detail=False,  # 是否在URL接口中添加一个pk路径参数
    url_path='archive/dates',
    url_name='archive-date',
    # 取消默认继承，修复API文档冗余信息
    filterset_class = None,
    pagination_class=None,
    )
  def list_archive_dates(self, request, *args, **kwargs):
    """
    获取文章归档时间列表
    """
    dates = Post.objects.dates('created_time', 'month', order='DESC')
    date_field = DateField()
    data = [date_field.to_representation(date)[:7] for date in dates]
    return Response(data=data, status=status.HTTP_200_OK)

  @action(
    methods=['GET'],
    detail=True,
    suffix='List',  # 将这个 action 返回的结果标记为列表，否则 drf-yasg 会根据 detail=True 误判为这是返回单个资源的接口
    filterset_class=None,  # 取消默认继承，API文档不需要过滤参数
    url_path='comments',
    url_name='comment',
    pagination_class=LimitOffsetPagination,
    serializer_class=CommentSerializer,
  )
  def list_comments(self, request, *args, **kwargs):
    """
    获取文章评论列表
    """
    post = self.get_object()  # 根据URL传入的参数值pk获取到文章对象
    queryset = post.comment_set.all()  # 获取文章下的全部评论
    page = self.paginate_queryset(queryset)  # 对评论列表进行分页，根据URL传入的参数获取指定页的评论
    serializer = self.get_serializer(page, many=True)  # 序列化评论
    return self.get_paginated_response(serializer.data)  # 返回分页后的评论列表


# class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#   serializer_class = CategorySerializer
#   permission_classes = [AllowAny]
#   queryset = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

# class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#   serializer_class = TagSerializer
#   queryset = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
#   permission_classes = [AllowAny]

class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  博客文章分类视图集

  list:
  返回博客文章分类列表
  """
  serializer_class = CategorySerializer
  pagination_class = None
  
  def get_queryset(self):
      return Category.objects.all().order_by('name')
  

class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  博客文章标签视图集

  list:
  返回博客文章标签列表
  """
  serializer_class = TagSerializer
  pagination_class = None  # 关闭分页
  throttle_classes = [TagAnonRateThrottle,]  # 接口限流
  
  def get_queryset(self):
      return Tag.objects.all().order_by('name')
  

class ApiVersionTestViewSet(viewsets.ViewSet):
  swagger_schema = None

  @action(
    methods=['GET'],
    detail=False,
    url_path='test',
    url_name='test',
    )
  def test(slef, request, *arg, **kwargs):
    if request.version == 'v1':
      return Response(data={'version': request.version, 'warning': '该接口的v1版本已废弃，请尽快迁移至v2版本'})
    return Response(data={'version': request.version})



