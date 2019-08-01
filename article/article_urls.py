"""PersonBlogSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from article import views
app_name = 'article' # 2.0版本之后需要进行设置
urlpatterns = [
    # path('<int:pagenum>/',views.index,name='indexp'), # 分页显示
    path('<slug:username>/detail/<slug:article_id>/', views.article_detail, name='article_detail'),
    path('nav/<slug:category_name>/', views.change_category, name='change_category'),  # 具体文章类， 显示改类的所有文章
    path('clear_history/', views.clear_history, name='clear_history'),  # 清楚浏览纪律
    path('search/', views.search_blog, name='search'),  # 搜索内容
    path('<slug:username>/publish/', views.article_publish, name='article_publish'),  # 文章发表
    path('comment/<slug:article_id>/', views.user_comment, name='user_comment'),  # 用户评论文章
    path('next_page_comment/', views.get_next_page_comment, name='get_next_page_comment'),

    path('test/', views.test, name='test'),
]
