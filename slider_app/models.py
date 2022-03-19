from django.db import models

# Create your models here.
from django.utils import html
from tinymce.models import HTMLField


class Slider(models.Model):
    STATUS = (
        ('u', 'منتشر نشود'),
        ('p', 'منتشر شود'),
    )
    title = HTMLField(verbose_name='عنوان', blank=True, null=True)
    image = models.ImageField(upload_to='images/slider/', verbose_name='تصویر', help_text='724*740', default=None,
                              blank=True, null=True)
    url = models.URLField(default=None, blank=True, null=True)

    status = models.CharField(max_length=100, choices=STATUS, default='u', verbose_name='وضعیت')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

    def __str__(self):
        return html.format_html(f'<p>{self.title}</p>')
