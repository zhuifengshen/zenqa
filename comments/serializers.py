from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['name', 'email', 'url', 'text', 'created_time', 'post']
    read_only_fileds = ['created_time']
    extra_kwargs = {'post': {'write_only': True}}  # post字段的值仅在创建评论时需要，在返回资源时不需要
