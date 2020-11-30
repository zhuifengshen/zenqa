from ..models import Comment
from .base import BaseTestCase


class CommentModelTestCase(BaseTestCase):
  def setUp(self):
    super().setUp()
    self.comment = Comment.objects.create(name='评论者', email='qq@qq.com', text='评论内容', post=self.post)
  
  def test_comment_representation(self):
    self.assertEqual(self.comment.__str__(), '评论者：评论内容')
