from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.utils import html


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='users/images/', verbose_name='عکس کاربر',
                              default=None, blank=True, null=True)
    education = models.CharField(max_length=1000, verbose_name='تحصیلات', blank=True, null=True)
    location = models.CharField(max_length=1000, verbose_name='موقعیت فعلی', blank=True, null=True)
    about_me = models.CharField(max_length=2000, verbose_name='درباره من', blank=True, null=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def get_photo(self):
        if self.photo:
            return html.format_html(f'<img src="{self.photo.url}" width=100 height=100 style="border-radius: 50%" />')
        else:
            return html.format_html(
                f'<img src="https://www.shareicon.net/data/512x512/2015/09/18/103159_user_512x512.png" width=100 height=100 style="border-radius: 50%" />')


class Skill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='مدل کاربر')
    skill = models.CharField(max_length=1000, verbose_name='مهارت')

    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت ها'

    def __str__(self):
        return self.skill
