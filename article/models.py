from ckeditor.fields import RichTextField
from django.db import models
from user.models import User
from mdeditor.fields import MDTextField


# 类别
class Category(models.Model):
    chinese_name = models.CharField(verbose_name='中文类名', max_length=10)
    foreign_name = models.CharField(verbose_name='英文', max_length=20)
    widget = models.SmallIntegerField(verbose_name='权重', default=500)

    def __str__(self):
        return self.chinese_name + '---' + self.foreign_name

    class Meta:
        verbose_name = '1.类别'
        verbose_name_plural = verbose_name


class Article(models.Model):
    # 文章表 一个作者----多个文章
    source_type_choices = ((1, '原创'), (2, '转载'))

    title = models.CharField(verbose_name='标题', max_length=256)
    content = MDTextField(verbose_name='文章内容')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    read_count = models.BigIntegerField(verbose_name='阅读数', default=0)
    source_type = models.SmallIntegerField(verbose_name='来源', choices=source_type_choices, default=1)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='文章类别')
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='作者')
    up_count = models.PositiveIntegerField(verbose_name='点赞的个数', default=0)
    down_count = models.PositiveIntegerField(verbose_name='踩的个数', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '2.文章'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    # 评论表
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='哪位用户的')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='评论的哪篇文章')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父评论')
    create_time = models.CharField(max_length=20, verbose_name='评论创建时间')
    content = RichTextField('评论内容')

    def __str__(self):
        return self.content[:10] + '...'

    class Meta:
        verbose_name = '3.评论'
        verbose_name_plural = verbose_name
