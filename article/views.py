import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from article.forms import ArticleForm, CommentForm
from article.models import *
from markdown import markdown
from PersonBlogSystem import settings

"""
导入的自定义的包
"""
from utils import get_random_banner, get_or_set_history, get_constraint, login_required, create_comment_element, \
    create_comment_elements, get_page_range


# Create your views here.
@get_constraint
def article_detail(request, username, article_id, **kwargs):
    article = Article.objects.filter(id=article_id, author__username=username)
    if not article:
        return HttpResponseNotFound()
    content = markdown(article[0].content)
    # 历史纪录
    history_time_list, new_history = get_or_set_history(request, article[0].id)
    comment_form = CommentForm()
    comment_list = article[0].comment_set.all().order_by('create_time')[:5]
    total_comment_count = article[0].comment_set.count()
    response = render(request, 'article/article_detail.html', {
        'article': article[0],
        'content': content,
        'history_time_list': history_time_list,
        'tool_bar': kwargs.get('tool_bar'),
        'comment_form': comment_form,
        'comment_list': comment_list,
        'total_comment_count': total_comment_count,
    })
    response.set_cookie('history', new_history)
    return response


@get_constraint
def change_category(request, category_name, page_capacity=5, **kwargs):
    category = Category.objects.filter(foreign_name=category_name)
    if not category:
        return HttpResponseForbidden()

    category_list = Category.objects.all()

    # 显示的文章
    page = int(request.GET.get('page', 1))
    article_list = Article.objects.filter(category=category[0]).order_by('-create_time')
    paginator = Paginator(article_list, page_capacity)
    total_page_count = paginator.num_pages
    if page > total_page_count:
        # return HttpResponseForbidden('访问页面不存在！！！')
        page = total_page_count
    page_object = paginator.page(page)
    display_page = get_page_range(page_object)

    banner_list, static_banner = get_random_banner()
    history_time_list = get_or_set_history(request)

    return render(request, 'article/change_category.html', {
        'category_list': category_list,
        'banner_list': banner_list,
        'static_banner': static_banner,
        'page_object': page_object,
        'paginator': paginator,
        'display_page': display_page,
        'category_name': category_name,
        'total_page_count': total_page_count,
        'tool_bar': kwargs.get('tool_bar'),
        'history_time_list': history_time_list,
    })


@get_constraint
def search_blog(request, page_capacity=5, **kwargs):
    """
    搜索文章
    :param request:
    :return:
    """
    category_list = Category.objects.all()
    keyword = request.GET.get('wd', '')
    if not keyword:
        return HttpResponseNotFound()

    article_list = Article.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by('id')
    page = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, page_capacity)
    total_page_count = paginator.num_pages
    if page > total_page_count:
        return HttpResponseForbidden('访问页面不存在！！！')
    page_object = paginator.page(page)
    display_page = get_page_range(page_object)

    return render(request, 'article/article_search_result.html', {
        'page_object': page_object,
        'display_page': display_page,
        'total_page_count': total_page_count,
        'category_list': category_list,
        'keyword': keyword,
        'tool_bar': kwargs.get('tool_bar'),
    })


def clear_history(request):
    """
    清除历史纪录
    :param requeet:
    :return:
    """
    response = JsonResponse({'status': 1})

    response.delete_cookie('history')

    return response


@get_constraint
def article_publish(request, username, **kwargs):
    user = request.session.get('user')

    if not user and user.username != username:
        return HttpResponseForbidden()

    if request.method == 'GET':
        article_form = ArticleForm()
        return render(request, 'article/article_publish.html', {
            'article_form': article_form,
            'tool_bar': kwargs.get('tool_bar'),
        })

    article_form = ArticleForm(request.POST)

    if article_form.is_valid():

        article = article_form.save(commit=False)
        article.author = user
        article.save()
        return redirect('blog:index')

    else:
        return render(request, 'article/article_publish.html', {
            'article_form': article_form,
            'tool_bar': kwargs.get('tool_bar'),
        })


@login_required
def user_comment(request, article_id):
    """
    用户评论文章的处理函数
    :param request:
    :param article_id:
    :return:
    """
    user = request.session.get('user')
    print(user)
    try:
        article = Article.objects.get(id=article_id)
    except Exception:
        return JsonResponse({'code': 'no', 'msg': '文章不存在!'})
    else:
        comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article_id = article_id
        comment.user = user
        comment.create_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        comment.save()
        article_comment_count = article.comment_set.count()
        data = create_comment_element(request, user, comment, article_comment_count)
        return JsonResponse({'code': 'ok', 'data': data})
    else:
        return JsonResponse({'code': 'no', 'msg': '数据格式错误！'})


def get_next_page_comment(request):
    print(request.POST)
    article_id = request.POST.get('article_id')
    comment_offset = int(request.POST.get('comment_offset'))
    data, count = create_comment_elements(article_id, comment_offset)
    return JsonResponse({'code': 'ok', 'data': data, 'count': count})


def test(request):
    """
    测试用的接口
    :param request:
    :return:
    """
    data = {
        'content': '<p>zxc</p>',
        'nickname': '超级管理员',
        'username': 'root',
        'head_img': '/user/head_img/1ee17cc85e5511e99f0b366895adad9f.jpg',
        'comment_id': 11
    }
    create_comment_element(data)
    return JsonResponse({
        'code': 'ok',
        'data': {
            'content': '<p>zxc</p>',
            'nickname': '超级管理员',
            'username': 'root',
            'head_img': '/static/media/user/head_img/1ee17cc85e5511e99f0b366895adad9f.jpg',
            'comment_id': 11
        },
    })
