# Generated by Django 4.0.1 on 2022-02-05 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings_app', '0005_rename_fave_icon_setting_fav_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='fav_icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons/', verbose_name='فاو آیکون'),
        ),
    ]