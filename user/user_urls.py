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
from user import views
app_name = 'user'
urlpatterns = [
    path('signin/', views.user_sign_in, name='user_sign_in'),
    path('signup/', views.user_sign_up, name='user_sign_up'),
    path('signout/', views.user_sign_out, name='user_sign_out'),
    # 验证码接
    path('vc/', views.generate_v_code, name='generate_v_code'),
    # 用户信息展示
    path('<slug:username>/',views.user_info, name='display_user_info')
]