from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Category, Post


class BaseTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create_superuser(username='admin', email='admin@qq.com', password='admin')
    self.cate = Category.objects.create(name='测试')
    self.post = Post.objects.create(title='测试标题', body='测试内容', category=self.cate, author=self.user)
