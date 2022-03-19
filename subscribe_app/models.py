from django.db import models
from django_jalali.db import models as jmodels


# Create your models here.

class Subscribe(models.Model):
    email = models.EmailField(verbose_name='ایمیل')
    date_send = jmodels.jDateTimeField(verbose_name='تاریخ عضویت')

    class Meta:
        verbose_name = 'خبر نامه'
        verbose_name_plural = 'خبر نامه ها'

    def __str__(self):
        return self.email
