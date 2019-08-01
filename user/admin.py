from django.contrib import admin
from user import models

# Register your models here.
# 注册Django admin 用户表和用户详情表
admin.site.register(models.User)
admin.site.register(models.UserInfo)