import os
import sys
import random
import pathlib
from datetime import timedelta
import faker

import django
from django.utils import timezone


# 将项目根目录添加到 Python 模块的搜索路径中，这样运行脚本才能找到响应的模块
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print('BASE_DIR: %s' % BASE_DIR)

def init():
  pass

def clean_db():
  print('clean database')
  Post.objects.all().delete()
  Category.objects.all().delete()
  Tag.objects.all().delete()
  Comment.objects.all().delete()
  User.objects.all().delete()

def create_db():
  print('create a superuser')
  user = User.objects.create_superuser('admin', 'admin@qa.com', 'admin')
  
  print('create categories')
  category_list = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
  for cate in category_list:
    Category.objects.create(name=cate)

  print('create tags')
  tag_list = ['django', 'Python', 'Pipenv', 'Docker', 'Nginx', 'Elasticsearch', 'Gunicorn', 'Supervisor', 'test tag']
  for tag in tag_list:
    Tag.objects.create(name=tag)

  print('create a markdown post')
  Post.objects.create(
    title='Markdown与代码高亮测试',
    body=pathlib.Path(BASE_DIR).joinpath('scripts', 'sample.md').read_text(encoding='utf-8'),
    category=Category.objects.create(name='Markdown测试'),
    author=user
  )

  print('create some english posts published within the past year')
  fake = faker.Faker()
  for _ in range(100):
    tags = Tag.objects.order_by('?')
    tag1 = tags.first()
    tag2 = tags.last()
    
    cate = Category.objects.order_by('?').first()
    created_time = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())

    post = Post.objects.create(
      title=fake.sentence().rstrip('.'),
      body='\n\n'.join(fake.paragraphs(10)),
      created_time=created_time,
      category=cate,
      author=user
    )
    post.tags.add(tag1, tag2)
    post.save()

  print('create some chinese posts published within the past year')
  fake = faker.Faker('zh_CN')
  for _ in range(100):
    tags = Tag.objects.order_by('?')
    tag1 = tags.first()
    tag2 = tags.last()
    
    cate = Category.objects.order_by('?').first()
    created_time = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())

    post = Post.objects.create(
      title=fake.sentence().rstrip('.'),
      body='\n\n'.join(fake.paragraphs(10)),
      created_time=created_time,
      category=cate,
      author=user
    )
    post.tags.add(tag1, tag2)
    post.save()


  print('create some comments')
  for post in Post.objects.all()[:20]:
    post_create_time = post.created_time
    delta_in_days = '-' + str((timezone.now() - post_create_time).days) + 'd'
    for _ in range(random.randrange(3, 15)):
      Comment.objects.create(
        name=fake.name(),
        email=fake.email(),
        url=fake.uri(),
        text=fake.paragraph(),
        created_time=fake.date_time_between(start_date=delta_in_days, end_date='now', tzinfo=timezone.get_current_timezone()),
        post=post
      )

  print('done!')


if __name__ == "__main__":
  # 初始化 Django 后，才能使用 Django 的 ORM 系统，以便创建数据
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zenofqa.settings.development')
  django.setup()
  from blog.models import Post, Category, Tag
  from comments.models import Comment
  from django.contrib.auth.models import User
  init()
  clean_db()
  create_db()

