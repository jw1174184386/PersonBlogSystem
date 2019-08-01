# -*- coding:utf-8 -*-
from django import forms
from django.middleware.csrf import CsrfViewMiddleware

from article.models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'source_type', 'category', 'author')
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control col-sm-6', 'required': '', 'placeholder': '文章标题', 'autofocus': ''}),
            'source_type': forms.Select(attrs={'class': 'form-control', 'required': ''}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': ''}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
