from django.db import models


# Create your models here.

class Setting(models.Model):
    logo = models.ImageField(upload_to='logos/', verbose_name='لوگوی سایت', help_text='26 * 103', blank=True, null=True)
    fav_icon = models.ImageField(upload_to='icons/', blank=True, null=True, verbose_name='فاو آیکون',
                                 help_text='80 * 80')
    name = models.CharField(max_length=1000, verbose_name='نام سایت', blank=True, null=True)
    copy_right = models.CharField(max_length=200000, verbose_name='نوشته قانون کی رایت', blank=True, null=True)

    class Meta:
        verbose_name = 'تنظیم سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return self.name


class Phone(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, verbose_name='شماره تلفن', blank=True, null=True)

    class Meta:
        verbose_name = 'شماره تلفن'
        verbose_name_plural = 'تلفن های سایت'

    def __str__(self):
        return self.phone_number


class Email(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='ایمیل', blank=True, null=True)

    class Meta:
        verbose_name = 'ایمیل سایت'
        verbose_name_plural = 'ایمیل های سایت'

    def __str__(self):
        return self.email


class Address(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    address = models.TextField(verbose_name='آدرس', blank=True, null=True)

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس  های شرکت'

    def __str__(self):
        return self.setting.name


class SocialNetwork(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    name = models.CharField(max_length=10000, verbose_name='نام شبکه', blank=True, null=True)
    url = models.URLField(verbose_name='آدرس اینترنتی', blank=True, null=True)

    class Meta:
        verbose_name = 'شبکه سایت'
        verbose_name_plural = 'شبکه های سایت'

    def __str__(self):
        return self.name


class SeoHomePage(models.Model):
    title = models.CharField(max_length=100, verbose_name='title', blank=True, null=True)
    keywords = models.CharField(max_length=100, verbose_name='keywords', blank=True, null=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)

    class Meta:
        verbose_name = 'سئو'
        verbose_name_plural = 'سثو صفحه ی اصلی'

    def __str__(self):
        return self.title
