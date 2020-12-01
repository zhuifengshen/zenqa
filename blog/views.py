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

from .models import Post, Category, Tag
from pure_pagination import PaginationMixin


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
