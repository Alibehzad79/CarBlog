# Generated by Django 4.0.1 on 2022-04-07 19:01

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0033_alter_article_category_alter_article_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_update',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ بروزرسانی'),
        ),
    ]
