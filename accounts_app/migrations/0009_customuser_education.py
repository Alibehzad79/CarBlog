# Generated by Django 4.0.1 on 2022-02-22 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0008_alter_customuser_about_me_alter_customuser_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='education',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='تحصیلات'),
        ),
    ]
