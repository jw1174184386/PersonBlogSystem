from django.db import models
from uuid import uuid4


# Create your models here.

class User(models.Model):
    """
        用户基本信息表
    """
    nickname = models.CharField(verbose_name='昵称', max_length=14)
    username = models.CharField(verbose_name='用户名', max_length=20)
    password = models.CharField(verbose_name='密码', max_length=20)
    head_img = models.ImageField(verbose_name='头像', upload_to='user/head_img') #头像上传的位置
    token = models.UUIDField(verbose_name='单点登陆', default=uuid4)

    def __str__(self):
        return '昵称：%s, 真实用户名：%s' % (self.nickname, self.username)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

class UserInfo(models.Model):
    """
        用户详细信息表
    """
    birthday = models.DateField(verbose_name='生日')
    country_choices = ((0, '中华人民共和国'), (1, '海外'))
    country = models.SmallIntegerField(choices=country_choices, verbose_name='国家')
    address = models.CharField(max_length=32, verbose_name='地址')
    user = models.OneToOneField(to='User', verbose_name='关联的用户', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.country_choices[self.country][1] + '---' + self.address

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
