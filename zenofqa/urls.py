"""zenofqa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from blog.feeds import AllPostsRssFeed

from rest_framework import routers, permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from blog.views import PostViewSet, CategoryViewSet, TagViewSet, ApiVersionTestViewSet
from comments.views import CommentViewSet

router = routers.DefaultRouter()
# 第一个参数是 URL 前缀，第二个参数是视图集，第三个参数视图函数名的前缀，默认生成规则是<namespace>:<basename>-<action name>
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'api-version', ApiVersionTestViewSet, basename='api-version')

schema_view = get_schema_view(
  openapi.Info(
    title='ZenQa REST framework API',
    default_version='v1',
    description='ZenQa API Document',
    terms_of_service='',
    contact=openapi.Contact(email='zhangchuzhao@dingtalk.com'),
    license=openapi.License(name='GPLv3 License'),
  ),
  public=True,
  permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('comments.urls')),
    path('rss/', AllPostsRssFeed(), name='rss'),
    path('api/v1/', include((router.urls, 'api'), namespace='v1')),
    path('api/v2/', include((router.urls, 'api'), namespace='v2')),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 文档
    re_path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
