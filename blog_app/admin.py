from django.contrib import admin

# Register your models here.
from django_jalali.admin.filters import JDateFieldListFilter

from blog_app.models import Article, Category, Tag, ArticleGallery, ArticleComment, Seo, SeoArticleList, SuggestionPost
import django_jalali.admin as jadmin


@admin.action(description='تغییر وضعیت به منتشر نشود')
def get_unpublished(modeladmin, request, queryset):
    queryset.update(status='u')


@admin.action(description='تغییر وضعیت به منتشر شود')
def get_published(modeladmin, request, queryset):
    queryset.update(status='p')


@admin.action(description='تغییر وصعیت به در حال بررسی')
def get_pending(modeladmin, request, queryset):
    queryset.update(status='w')


class ArticleGalleryTabularInline(admin.TabularInline):
    model = ArticleGallery


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('get_image', '__str__', 'creator', 'visit_count', 'date_created', 'date_update', 'status')
    list_filter = (
        ('date_created', JDateFieldListFilter), ('date_update', JDateFieldListFilter), 'status', 'creator', 'category',
        'tag')
    list_editable = ('status',)
    search_fields = ('title', 'content', 'category', 'tag')
    actions = [get_unpublished, get_published, get_pending]
    inlines = [ArticleGalleryTabularInline]


Article.get_image.short_description = 'تصویر'


@admin.action(description='قبول کردن')
def get_accept(modeladmin, request, queryset):
    queryset.update(status='a')


@admin.action(description='قبول نکردن')
def get_dont_accept(modeladmin, request, queryset):
    queryset.update(status='r')


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'status')
    list_editable = ('status',)
    actions = [get_accept, get_dont_accept]
    list_filter = ('date_send', 'status')
    search_fields = ('email', 'name', 'text')


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Seo)
admin.site.register(SeoArticleList)
admin.site.register(SuggestionPost)
