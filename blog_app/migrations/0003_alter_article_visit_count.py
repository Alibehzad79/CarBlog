# Generated by Django 4.0.1 on 2022-01-31 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_alter_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='visit_count',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
