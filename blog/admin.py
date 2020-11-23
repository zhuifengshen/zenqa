from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.
class PostAdmin(admin.ModelAdmin):
  list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
  fields = ['title', 'body', 'excerpt', 'category', 'tags']

  def save_model(self, request, obj, form, change):
    """
    将此ModelAdmin关联注册的Model实例保存到数据库
    request：此次HTTP请求对象
    obj：此次创建的关联对象的实例
    """
    obj.author = request.user
    super().save_model(request, obj, form, change)

    
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
