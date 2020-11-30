
from django.contrib.auth.models import User
from django.template import Context, Template
from django.test import TestCase

from ..models import Post, Category, Tag
from ..templatetags.blog_extras import show_archives, show_categories, show_recent_posts, show_tags


class BlogExtrasTestCase(TestCase):
  
  def setUp(self):
    self.user = User.objects.create_superuser(username='admin', email='admin@qq.com', password='admin')
    self.cate = Category.objects.create(name='测试')
    self.ctx = Context()

  def test_show_recent_posts(self):
    post = Post.objects.create(title='测试标题', body='测试内容', category=self.cate, author=self.user)
    context = Context(show_recent_posts(self.ctx))
    template = Template('{% load blog_extras %} {% show_recent_posts %}')
    expected_html = template.render(context)
    self.assertInHTML('<h3 class="widget-title">最新文章</h3>', expected_html)
    self.assertInHTML('<a href="{}">{}</a>'.format(post.get_absolute_url(), post.title), expected_html)
