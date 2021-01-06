from django.urls import path

from . import views

app_name = 'blog'  # 视图函数命名空间

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('posts/<int:pk>/', views.detail, name='detail'),
#     path('archive/<int:year>/<int:month>/', views.archive, name='archive'),
#     path('category/<int:pk>/', views.category, name='category'),
#     path('tag/<int:pk>/', views.tag, name='tag'),
# ]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archive/<int:year>/<int:month>/', views.archive, name='archive'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    # path('api/index/', views.index),
    path('api/index/', views.IndexPostListAPIView.as_view()),
]
