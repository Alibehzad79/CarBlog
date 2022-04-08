from django.urls import path

from api.views import ArticleListApiView, ArticleDetailApiView, ArticleUpdateApiView, ArticleDeleteApiView, \
    CreateArticleApiView

app_name = 'api'
urlpatterns = [
    path('', ArticleListApiView.as_view(), name='api-article-list'),
    path('create-article/', CreateArticleApiView.as_view(), name='api-create-article'),
    path('<int:pk>/', ArticleDetailApiView.as_view(), name='api-article-detail'),
    path('<int:pk>/update/', ArticleUpdateApiView.as_view(), name='api-article-update'),
    path('<int:pk>/delete/', ArticleDeleteApiView.as_view(), name='api-article-delete'),
]
