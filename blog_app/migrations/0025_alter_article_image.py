# Generated by Django 4.0.1 on 2022-02-03 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0024_suggestionpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, help_text='440 * 750', upload_to='blog/images/', verbose_name='تصویر پست'),
        ),
    ]
