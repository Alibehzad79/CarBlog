from django.db import models
from django_jalali.db import models as jmodels


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=25, verbose_name='نام و نام خانوادگی', blank=True, null=True)
    email = models.EmailField(verbose_name='ایمیل', blank=True, null=True)
    subject = models.CharField(max_length=1000, verbose_name='عنوان تماس', blank=True, null=True)
    message = models.TextField(verbose_name='پیغام', blank=True, null=True)
    date_send = jmodels.jDateTimeField(verbose_name='تاریخ ارسال', blank=True, null=True)

    class Meta:
        verbose_name = 'تماس کاربر'
        verbose_name_plural = 'تماس های کاربران'

    def __str__(self):
        return self.name
