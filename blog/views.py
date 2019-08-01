from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render
from article.models import *
from blog.models import *
from utils import get_random_banner, get_or_set_history, get_constraint, get_page_range


# Create your views here.

@get_constraint
def index(request, page_capacity=5, **kwargs): # 设置单页显示容量，默认为5
    if request.method == 'POST':
        return HttpResponseForbidden()

    category_list = Category.objects.all()  # 获取所有的类别

    # 显示的文章
    page = int(request.GET.get('page', 1)) # 如果page值不存在，默认显示第一页数据
    article_list = Article.objects.order_by('-create_time') # 获取文章列表，按照生成的时间逆序
    paginator = Paginator(article_list, page_capacity) # 分页器
    total_page_count = paginator.num_pages  # 需要的总页数
    if page > total_page_count:
        page = total_page_count
    page_object = paginator.page(page)  # 当前传入的page值
    display_page = get_page_range(page_object)  # 返回生成的5个页码

    banner_list, static_banner = get_random_banner()
    history_time_list = get_or_set_history(request)

    return render(request, 'blog/blog.html', {
        'category_list': category_list,
        # 'article_list': article_list,
        'banner_list': banner_list,
        'paginator': paginator,
        'page_object': page_object,
        'display_page': display_page,
        'static_banner': static_banner,
        'total_page_count': total_page_count,
        'history_time_list': history_time_list,
        'tool_bar': kwargs.get('tool_bar'),
    })
