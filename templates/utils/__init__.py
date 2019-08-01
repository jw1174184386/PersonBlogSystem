"""
一些项目中用到的方法
"""

from django.shortcuts import redirect
from graduation_project.settings import MEDIA_URL
import random
import hashlib
import time

from user.models import User
from article.models import Comment, Article
from blog.models import *


def get_random_banner():
    """
    轮播图随机显示
    :return:
    """
    total_banner_count = Banner.objects.count()
    if total_banner_count < 5:
        banner_list = list(Banner.objects.all())

        static_banner = []
    else:
        # print(total_banner_count)
        random_num = random.randint(0, total_banner_count - 5)
        # print(random_num)
        banner_list = list(Banner.objects.all()[random_num:random_num + 3])
        # print(banner_list, '----')
        static_banner = list(Banner.objects.all()[random_num + 3:random_num + 5])
        # print(static_banner)
    random.shuffle(banner_list)
    random.shuffle(static_banner)
    return banner_list, static_banner


def get_constraint(view_func):
    """
    拿到一些平时不变的变量，view_func必须要有**kwargs参数
    :return:
    """

    def inner(request, *args, **kwargs):
        tool_bar = Toolbar.objects.all()
        return view_func(request, tool_bar=tool_bar, *args, **kwargs)

    return inner


def get_token(username):
    """
    根据uid 和 username 来生成token
    :param uid:
    :param username:
    :return:
    """
    hash_string = str(time.time()) + username
    md = hashlib.md5()
    md.update(hash_string.encode())
    return md.hexdigest()


def login_required(views_func):
    """
    是否登录的判断
    登录：运训
    未登录：跳转到登录页面
    :param views_func: 视图函数
    :return:
    """

    def inner(request, *args, **kwargs):
        token = request.COOKIES.get('token')
        print(token)
        user = User.objects.filter(token=token)
        print(user)
        if not user:
            return redirect('user:user_sign_in')
        return views_func(request, *args, **kwargs)

    return inner


def get_or_set_history(request, article_id=None):
    """
    获取和设置历史纪录
    :param request:
    :return:
    """
    old_history = request.COOKIES.get('history', '')
    if article_id:
        if old_history:  # 如果原来有历史纪录
            time_now = int(time.time())  # 时间戳

            if str(article_id) + '-' in old_history:

                new_history = ''
                for history_time in old_history.split(','):
                    if not history_time.startswith(str(article_id) + '-'):
                        new_history = history_time + ',' + new_history
                new_history = str(article_id) + '-' + str(time_now) + ',' + new_history
            else:
                new_history = str(article_id) + '-' + str(time_now) + ',' + old_history

        else:
            new_history = str(article_id) + '-' + str(int(time.time()))

        history_time_list = []  # 格式为[(article_id,time),(),()]
        for history_time in new_history.split(','):
            if history_time:
                history_time = history_time.split('-')

                art = Article.objects.filter(id=history_time[0]).first()

                # 转换成新的时间格式(2016-05-09 18:59:20)
                history_time[0] = art
                history_time[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(history_time[1])))
                history_time_list.append(history_time)

        # print(history_time_list)
        return [history_time_list, new_history]
    else:
        history_time_list = []  # 格式为[(article_id,time),(),()]
        for history_time in old_history.split(','):
            if history_time:
                history_time = history_time.split('-')

                art = Article.objects.filter(id=history_time[0]).first()

                # 转换成新的时间格式(2016-05-09 18:59:20)
                history_time[0] = art
                history_time[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(history_time[1])))
                history_time_list.append(history_time)
        return history_time_list


def create_comment_element(request=None, user=None, comment=None, comment_count=None, data=None):
    """
    创建评论的div元素
    :param request:
    :param user: 用户对象
    :param comment: 评论对象
    :return:
    """
    if not data:
        data = {
            'next_floor': comment_count,
            'content': request.POST.get('content'),
            'nickname': user.nickname,
            'head_img': str(user.head_img),
            'comment_id': comment.id,
            'username': user.username,
            'create_time': comment.create_time,
        }

    inner_html = """<div>{next_floor}楼</div>
    <div style="display: inline-block;margin-right: 20px;">
        <img src="{MEDIA_URL}{head_img}" style="width: 48px;height: 48px;">
    </div>
    <div style="display: inline-block;">
        {content}
    </div>
    <div>
        <div style="display: inline-block;">
            <a href="/user/{username}">{nickname}</a>
        </div>
        <div style="display: inline-block; margin-left: 20px;">
            <span>{create_time}</span>
        </div>
    </div>
    <hr>"""
    data = inner_html.format(MEDIA_URL=MEDIA_URL, **data)
    return data


def create_comment_elements(article_id, comment_offset, limit=5):
    if not article_id or not comment_offset:
        # 只要存在一个没有，
        raise Exception('article_id 和 comment_offset都不能为空！')
    try:
        article = Article.objects.get(id=article_id)
        next_page_comment = article.comment_set.all().order_by('create_time')[comment_offset:comment_offset + limit]
    except Exception as e:
        print(e)
    else:
        result_html = ''
        start_floor = comment_offset
        for comment in next_page_comment:
            start_floor += 1
            data = {
                'next_floor': start_floor,
                'content': comment.content,
                'nickname': comment.user.nickname,
                'head_img': str(comment.user.head_img),
                'comment_id': comment.id,
                'username': comment.user.username,
                'create_time': comment.create_time,
            }
            result_html += create_comment_element(data=data)
        return result_html, len(next_page_comment)


def get_page_range(page, display_page=4):
    """
    获取分页页数的范围
    :param page: page对象
    :param dispage: 要显示的页数 ---  上一页《《 1， 2， 3， 4， 5，》》下一页
    :return:
    """
    if page.paginator.num_pages < display_page:
        page_range = range(1, page.paginator.num_pages + 1)
    else:
        if page.number <= display_page // 2:
            page_range = range(1, display_page + 1)
        else:
            if page.number + 2 > page.paginator.num_pages:
                page_range = range(page.paginator.num_pages - display_page + 1, page.paginator.num_pages + 1)
            else:
                page_range = range(page.number - display_page // 2, page.number + display_page // 2 + 1)
    return page_range


def format_time(f_time=''):
    f_time = f_time.replace('-0', '-')
    # 2019-5-9
    f_time = f_time[:4] + '年' + f_time[5:] + '日'
    f_time = f_time.replace('-', '月')
    return f_time
