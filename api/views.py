from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework import permissions as perms
from api.serializers import ArticleSerializer
# Create your views here.
from blog_app.models import Article


class ArticleListApiView(ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class CreateArticleApiView(CreateAPIView, ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [perms.IsAdminUser]


class ArticleDetailApiView(RetrieveAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [perms.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(creator=self.request.user).all()


class ArticleUpdateApiView(UpdateAPIView, RetrieveAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [perms.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(creator=self.request.user).all()


class ArticleDeleteApiView(DestroyAPIView, RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [perms.IsAuthenticated]
