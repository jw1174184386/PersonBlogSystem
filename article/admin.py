from django.contrib import admin

# Register your models here.
from article.models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'article', 'create_time')
    list_display_links = ('user',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'read_count', 'create_time', 'source_type', 'author']

    list_display_links = ('title',)
    date_hierarchy = 'create_time'
    search_fields = ('title', 'content')
    list_filter = ('source_type',)

    # 添加action动作
    actions = ('sourceTypeToOrigin', 'sourceTypeToReprint')

    def source_type_to_origin(self, request, queryset):
        queryset.update(source_type='1')

    source_type_to_origin.short_description = '【来源】类型改为【原创】'

    def source_type_to_reprint(self, request, queryset):
        queryset.update(source_type='2')

    source_type_to_reprint.short_description = '【来源】类型改为【转载】'

admin.site.site_header = '风城浪子博客园后台管理系统'
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
