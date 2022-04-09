from rest_framework.serializers import ModelSerializer

from blog_app.models import Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        exclude =['creator']
