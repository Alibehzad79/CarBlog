# Generated by Django 4.0.1 on 2022-02-04 16:38

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('date_send', django_jalali.db.models.jDateTimeField()),
            ],
            options={
                'verbose_name': 'خبر نامه',
                'verbose_name_plural': 'خبر نامه ها',
            },
        ),
    ]
