from django.urls import path

from api.views import ArticleListApiView

app_name = 'api'
urlpatterns = [
    path('', ArticleListApiView.as_view(), name='api-article-list'),
]
