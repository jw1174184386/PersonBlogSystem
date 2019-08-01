# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from user.models import User, UserInfo


class UserSignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'required': '', 'placeholder': '用户名', 'autofocus': ''}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': '', 'placeholder': '密码'}),

        }


class UserSignUpForm(forms.ModelForm):
    """
    如果不符合要求， 抛出 ValidationError 异常
    正确返回 对应的字段值
    """

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5 or len(username) > 14:
            raise ValidationError('帐号长度在6-14之间')

        user = User.objects.filter(username=username)
        if user:
            # 如果帐号已经存在，抛出异常
            raise ValidationError('帐号已经存在')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password[0].isalpha():
            raise ValidationError('密码要以字符为开头')

        if len(password) < 5 or len(password) > 15:
            raise ValidationError('密码长度在6-14之间')

        return password

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        user = User.objects.filter(nickname=nickname)
        if user:
            raise ValidationError('昵称已经存在')
        return nickname

    class Meta:
        model = User
        # 指定字段名
        fields = ('nickname', 'username', 'password', 'head_img')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'required': '', 'placeholder': '用户名', }),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': '', 'placeholder': '密码'}),
            'nickname': forms.TextInput(
                attrs={'class': 'form-control', 'required': '', 'placeholder': '昵称', 'autofocus': ''}),

            'head_img': forms.FileInput(),
        }


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('birthday', 'country', 'address')
