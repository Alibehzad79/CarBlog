# Generated by Django 4.0.1 on 2022-02-03 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0018_remove_articlecomment_is_accept_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='visit_count',
            field=models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید'),
        ),
    ]
