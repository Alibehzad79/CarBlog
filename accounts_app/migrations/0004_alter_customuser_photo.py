# Generated by Django 4.0.1 on 2022-01-30 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0003_alter_customuser_managers_customuser_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, default='media/users/images/TurkAli.jpg', null=True, upload_to='users/images/', verbose_name='عکس کاربر'),
        ),
    ]
