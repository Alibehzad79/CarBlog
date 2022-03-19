import datetime

from django.db import models
from django.db.models import Q
from django.utils import html
from tinymce.models import HTMLField
from django_jalali.db import models as jmodels
# Create your models here.
from config.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=1000, verbose_name='دسته بندی', blank=True, null=True)
    slug = models.SlugField(max_length=1000, verbose_name='نام انگلیسی', help_text='برای مثال: category-name',
                            blank=True, null=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=1000, verbose_name='دسته بندی', blank=True, null=True)
    slug = models.SlugField(max_length=1000, verbose_name='نام انگلیسی', help_text='برای مثال: tag-name', blank=True,
                            null=True)

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):
    def get_search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(category__name__icontains=query) |
                Q(tag__name__icontains=query)
        )
        return self.get_queryset().filter(lookup, status='p').distinct()


class Article(models.Model):
    STATUS = (
        ('u', 'منتشر نشود'),
        ('w', 'درحال بررسی'),
        ('p', 'منتشر شود'),
    )

    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='نویسنده', blank=True,
                                null=True)
    title = models.CharField(max_length=1000, verbose_name='عنوان پست', blank=True, null=True)
    content = HTMLField(verbose_name='توضیحات', blank=True, null=True)
    image = models.ImageField(upload_to='blog/images/', verbose_name='تصویر پست', help_text="440 * 750", blank=True,
                              null=True)
    video_url = models.URLField(verbose_name='لینک ویدئو آپارات', default='', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='انتخاب دسته بندی', blank=True,
                                 null=True)
    tag = models.ManyToManyField(Tag, verbose_name='انتخاب برچسب', blank=True)
    date_created = jmodels.jDateTimeField(verbose_name='تاریخ ایجاد', blank=True, null=True, auto_now_add=True)
    date_update = jmodels.jDateTimeField(verbose_name='تاریخ بروزرسانی', blank=True, null=True, auto_now_add=True)
    status = models.CharField(max_length=1000, choices=STATUS, default='u', verbose_name='وضعیت', blank=True, null=True)
    visit_count = models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید', blank=True, null=True)

    objects = ArticleManager()

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return html.format_html(f'<img src="{self.image.url}" width=100 height=100 style="border-radius: 5px" />')
        else:
            return None

    def get_video_url(self):
        return self.video_url.strip('https://www.aparat.com/v/')

    def get_slug_title(self):
        return self.title.replace(' ', '-')

    def get_all_visit_count(self):
        pass


class ArticleGallery(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='پست', blank=True, null=True)
    title = models.CharField(max_length=1000, verbose_name='عنوان', blank=True, null=True)
    image = models.ImageField(upload_to='article/gallery/', verbose_name='تصویر', blank=True, null=True,
                              help_text="353 * 466")

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'گالری'

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    STATUS = (
        ('a', 'قبول شود'),
        ('r', 'رد شود'),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='پست', blank=True, null=True)
    name = models.CharField(max_length=10000, verbose_name='نام و نام خانوادگی', blank=True, null=True)
    email = models.EmailField(verbose_name='ایمیل', blank=True, null=True)
    text = models.TextField(verbose_name='پیغام', blank=True, null=True)
    date_send = jmodels.jDateTimeField(verbose_name='تاریخ ارسال', blank=True, null=True)
    status = models.CharField(max_length=1000, choices=STATUS, default='r', verbose_name='وضعیت', blank=True, null=True)

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return self.email


class Seo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, verbose_name="پست")
    title = models.CharField(max_length=1000, verbose_name='title', blank=True, null=True)
    keywords = models.CharField(max_length=1000, verbose_name='keywords', blank=True, null=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)

    class Meta:
        verbose_name = 'سئو'
        verbose_name_plural = 'سثو پست ها'

    def __str__(self):
        return self.article.title


class SeoArticleList(models.Model):
    title = models.CharField(max_length=1000, verbose_name='title', blank=True, null=True)
    keywords = models.CharField(max_length=10000, verbose_name='keywords', blank=True, null=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)

    class Meta:
        verbose_name = 'سئو'
        verbose_name_plural = 'سثو صفحه ی لیست پست ها'

    def __str__(self):
        return self.title


class SuggestionPost(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='پست')

    class Meta:
        verbose_name = 'پست پیشنهادی'
        verbose_name_plural = 'پست های پیشنهادی مدیر'

    def __str__(self):
        return self.article.title
