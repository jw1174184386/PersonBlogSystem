# user应用
# 用于用户注册登录，验证码处理
import io
import random

from PIL import Image, ImageDraw, ImageFont
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect

from PersonBlogSystem.settings import BASE_DIR
from user import forms
from user.forms import UserInfoForm
from user.models import *
from utils import *


# Create your views here.


def user_sign_in(request):
    # 用户登录
    if request.method == 'GET':
        # 获取传过来的token值，用于数据库验证
        token = request.COOKIES.get('token')
        # 数据库过滤，判断该用户是否是否存在，或者cookie时间未过期
        user = User.objects.filter(token=token)
        if not user:
            # 如果没有用户
            form = forms.UserSignInForm()
            return render(request, 'user/sign_in.html', {
                'form': form,
            })
        # 重定向到主页面
        return redirect('blog:index')

    form = forms.UserSignInForm(request.POST)
    # post请求
    if form.is_valid():
        # 判断当前用户是否存在以及用户信息是否正确
        v_code = request.POST.get('v_code')
        if v_code and v_code == request.session.get('v_code'):
            user = User.objects.filter(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # 查询到的是queryset.
            if user:
                token = get_token(user[0].username)
                user[0].token = token
                user[0].save()

                response = redirect('blog:index')
                # 设置token验证，3天时间
                response.set_cookie('token', token, expires=1209600)
                request.session['user'] = user[0]
                return response

            else:
                # print('用户没找到',form.errors)
                error = '帐号或密码错误！'
                return render(request, 'user/sign_in.html', {
                    'form': form,
                    'error': error,
                })
        else:
            error = '验证码错误！'
            return render(request, 'user/sign_in.html', {
                'form': form,
                'error': error,
            })
    else:

        error = '帐号或密码错误！'
        return render(request, 'user/sign_in.html', {
            'form': form,
            'error': error,
        })


def user_sign_up(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == 'GET':
        token = request.COOKIES.get('token')
        user = User.objects.filter(token=token)
        if not user:
            # 如果没有用户
            form = forms.UserSignUpForm()
            return render(request, 'user/sign_up.html', {
                'form': form,
            })
        return redirect('blog:index')

    form = forms.UserSignUpForm(request.POST, files=request.FILES)

    if form.is_valid():
        # 如果数据没有问题，那么就可以保存了，注册成功，返回到博客首页
        user = form.save(commit=False)
        user.token = get_token(user.username)
        user.save()

        response = redirect('blog:index')
        response.set_cookie('token', user.token, expires=1209600)
        request.session['user'] = user
        return response

    else:

        return render(request, 'user/sign_up.html', {
            'form': form,
        })


def generate_v_code(request):
    """
    生成验证码
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 新生成一个图片
        im = Image.new('RGB', (120, 40), (123, 123, 123))
        # 启用画笔进行绘制
        draw = ImageDraw.Draw(im, 'RGB')
        # 设置字体的属性、颜色、大小
        font = ImageFont.truetype(font=BASE_DIR + '/static/font/simfang.ttf', size=20)
        # data = random.sample(string.ascii_letters + string.digits, 4)
        # 验证码 随机产生的 两个数字的 加减乘
        data = list()
        data.append(str(random.randint(1, 18)))
        data.append(random.sample('+-*', 1)[0])
        data.append(str(random.randint(1, 10)))

        x_offset = 15 # 给定偏移量数值
        for d in data:
            # 20  40  60  80  100
            draw.text(xy=(x_offset, 10), text=d, font=font)
            x_offset += 30
        bio = io.BytesIO()
        im.save(bio, 'PNG')
        v_code_result = eval(''.join(data))
        request.session['v_code'] = str(v_code_result)  # 将验证码中防止session中
        return HttpResponse(content=bio.getvalue(), content_type='image/png')
    else:
        return HttpResponseForbidden()


@login_required
def user_sign_out(request):
    """
    用户注销登录
    :param request:
    :return:
    """
    del request.session['user']
    response = redirect('blog:index')
    response.delete_cookie('token')

    return response


@get_constraint
def user_info(request, page_capacity=5, *args, **kwargs):
    """
    用户信息更改或者显示
    :param request:
    :param args:
    :param page_capacity:页容量
    :param kwargs:
    :return:
    """
    if request.method == 'GET':
        user = User.objects.filter(username=kwargs.get('username')).first()
        if not user:
            return HttpResponseNotFound()

        username = kwargs.get('username')
        # 判断是否是本人的主页，如果是，那么就显示可以更改的状态。
        if request.session.get('user') and request.session.get('user').username == username:
            change_info_flag = True

        else:
            change_info_flag = False

        article_list = user.article_set.all().order_by('-id')
        page = int(request.GET.get('page', 1))
        paginator = Paginator(article_list, page_capacity)
        total_page_count = paginator.num_pages
        if page > total_page_count:
            return HttpResponseForbidden('访问页面不存在！！！')
        page_object = paginator.page(page)
        display_page = get_page_range(page_object)

        context = {
            "username": kwargs.get('username'),
            'user': user,
            'article_list': article_list,
            'page_object': page_object,
            'display_page': display_page,
            'total_page_count': total_page_count,
            'tool_bar': kwargs.get('tool_bar'),
            'change_info_flag': change_info_flag,
        }

        response = render(request, 'user/user_info.html', context)
        return response

    elif request.method == 'POST':
        # 如果是POST请求，说明是要更改用户信息
        user = request.session.get('user')
        if not user:
            return HttpResponseForbidden()
        if user.username != kwargs.get('username'):
            return HttpResponseForbidden
        print(request.POST)

        form_data = dict(request.POST)
        form_data['user_id'] = [user.id]
        form_data = {k: v[0] for k, v in form_data.items()}

        user_info_form = UserInfoForm(form_data, instance=user.userinfo)
        if user_info_form.is_valid():
            user_info_form.save()
            data = {'code': 'yes', 'data': {
                'birthday': format_time(form_data['birthday'])
            }}
        else:
            print(user_info_form.errors)
            data = {'code': 'noe', 'error': user_info_form.errors}
        return JsonResponse(data)
    else:
        return HttpResponseForbidden()
