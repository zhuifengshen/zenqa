from django.urls import reverse

from .base import BaseTestCase
from ..models import Comment


class CommentViewTestCase(BaseTestCase):
  def setUp(self):
    super().setUp()
    self.url = reverse('comments:comment', kwargs={'post_pk': self.post.pk})
  
  def test_comment_a_inexistence_post(self):
    url = reverse('comments:comment', kwargs={'post_pk': 100})
    response = self.client.post(url, {})
    self.assertEqual(response.status_code, 404)
  
  def test_invalid_comment_data(self):
    invalid_data = {
      'email': 'invalid_email'
    }
    response = self.client.post(self.url, invalid_data)
    self.assertTemplateUsed(response, 'comments/preview.html')
    self.assertIn('post', response.context)
    self.assertIn('form', response.context)
    form = response.context['form']
    for field_name, errors in form.errors.items():  # 一旦表单绑定了数据，并且 is_valid 方法被调用，就会有一个 errors 属性
      for err in errors:
        self.assertContains(response, err)
    self.assertContains(response, '评论发表失败！请修改表单中的错误后重新提交。')
  
  def test_valid_comment_data(self):
    valid_data = {
      'name': '评论者',
      'email': 'admin@qq.com',
      'url': 'https://qq.com',
      'text': '评论内容'
    }
    response = self.client.post(self.url, valid_data, follow=True)  # 跟踪重定向
    self.assertRedirects(response, self.post.get_absolute_url())
    self.assertContains(response, '评论发表成功！')
    self.assertEqual(Comment.objects.count(), 1)
    comment = Comment.objects.first()
    self.assertEqual(comment.name, valid_data['name'])
    self.assertEqual(comment.text, valid_data['text'])


