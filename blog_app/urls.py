from django.urls import path

from blog_app.views import ArticleListView, article_detail_view, Search, GetByCategory, GetByTag

app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:article_id>/<title>/', article_detail_view, name='article_detail'),
    path('search/', Search.as_view(), name='search'),
    path('categories/<slug:category_name>/', GetByCategory.as_view(), name='get_category'),
    path('tags/<slug:tag_name>/', GetByTag.as_view(), name='get_tag'),
]
