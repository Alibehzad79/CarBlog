from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class AboutUs(models.Model):
    title = models.CharField(max_length=1000, verbose_name='عنوان', blank=True, null=True)
    content = HTMLField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'

    def __str__(self):
        return self.title


class Team(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, verbose_name='درباره ما', blank=True, null=True)
    name = models.CharField(max_length=1000, verbose_name='تام و نام خانوادگی', blank=True, null=True)
    job = models.CharField(max_length=1000, verbose_name='شغل', blank=True, null=True)
    image = models.ImageField(upload_to='images/teams/', verbose_name='تصویر', blank=True, null=True)

    class Meta:
        verbose_name = 'عضو'
        verbose_name_plural = 'اعضا'

    def __str__(self):
        return self.name
