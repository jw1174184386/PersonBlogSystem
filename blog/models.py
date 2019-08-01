from django.db import models
from article.models import Article


# Create your models here.


# 导航
class Toolbar(models.Model):
    tool_name = models.CharField(verbose_name='工具块名', max_length=10)
    url = models.CharField(verbose_name='url链接', max_length=100)

    def __str__(self):
        return self.tool_name + '---' + self.url

    class Meta:
        verbose_name = '导航工具栏'
        verbose_name_plural = verbose_name


# 广告
class Advertise(models.Model):
    url = models.CharField(verbose_name='广告路径', max_length=100)
    img = models.ImageField(verbose_name='图片', upload_to='banner')
    name = models.CharField(verbose_name='广告名字', max_length=20)
    widget = models.SmallIntegerField(verbose_name='权重')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name


# 轮播图
class Banner(models.Model):
    img_url = models.ImageField(verbose_name='图片', upload_to='banner', null=True, blank=True)
    article = models.OneToOneField(Article, on_delete=models.SET_NULL, null=True, blank=True)
    widget = models.SmallIntegerField(verbose_name='权重', default=500)

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
