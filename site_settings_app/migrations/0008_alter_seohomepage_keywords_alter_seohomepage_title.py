# Generated by Django 4.0.1 on 2022-02-06 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings_app', '0007_alter_setting_fav_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seohomepage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='keywords'),
        ),
        migrations.AlterField(
            model_name='seohomepage',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='title'),
        ),
    ]
