from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from api.serializers import ArticleSerializer
# Create your views here.
from blog_app.models import Article


class ArticleListApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
