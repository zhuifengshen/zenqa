from django.contrib.auth.models import User
from django.template import Template, Context

from blog.models import Post, Category
from .base import BaseTestCase
from ..forms import CommentForm
from ..templatetags.comments_extras import show_comment_form, show_comments


class CommentExtraTestCase(BaseTestCase):
  def setUp(self):
    super().setUp()
    self.ctx = Context()

  def test_show_comment_form_with_invalid_data(self):
    template = Template('{% load comments_extras %} {% show_comment_form post form %}')
    invalid_data = {'email': 'invalid_email'}
    form = CommentForm(data=invalid_data)
    self.assertFalse(form.is_valid())
    context = Context(show_comment_form(self.ctx, self.post, form=form))
    expected_html = template.render(context)
    for field in form:
      label = '<label for="{}">{}：</label>'.format(field.id_for_label, field.label)
      self.assertInHTML(label, expected_html)
      self.assertInHTML(str(field), expected_html)
      self.assertInHTML(str(field.errors), expected_html)
  
