import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView

from blog_app.forms import ArticleCommentForm
from blog_app.models import Article, Category, Tag, ArticleComment, Seo, SeoArticleList
from site_settings_app.models import Setting


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    paginate_by = 4

    def get_queryset(self):
        return Article.objects.filter(status='p').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['meta_tag'] = SeoArticleList.objects.last()
        context['setting'] = Setting.objects.last()
        return context


def article_detail_view(request, *args, **kwargs):
    article_id = kwargs['article_id']
    article = Article.objects.filter(id=article_id, status='p').exists()
    if not article:
        raise Http404()
    article = Article.objects.get(id=article_id, status='p')
    form = ArticleCommentForm(request.POST or None, initial={"article_id": article_id})
    if form.is_valid():
        email = form.cleaned_data.get('email')
        name = form.cleaned_data.get('name')
        text = form.cleaned_data.get('text')
        article_id = form.cleaned_data.get('article_id')
        article = Article.objects.filter(id=article_id).first()

        new_comment = ArticleComment.objects.create(email=email, name=name, text=text, article=article,
                                                    status='r', date_send=datetime.datetime.now())
        if new_comment is not None:
            new_comment.save()
            return redirect('blog:article_detail', article.id, article.get_slug_title())
        form = ArticleCommentForm()

    comments = ArticleComment.objects.filter(status='a', article=article).all()
    article.visit_count += 1
    article.save()
    meta_tag = Seo.objects.filter(article=article).last()
    setting = Setting.objects.last()
    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'meta_tag': meta_tag,
        'setting': setting,
    }
    return render(request, 'blog/article_detail.html', context)


def sidebar(request):
    recent_articles = Article.objects.filter(status='p').order_by('-id').all()[:4]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    setting = Setting.objects.last()
    context = {
        'recent_articles': recent_articles,
        'categories': categories,
        'tags': tags,
        'setting': setting,
    }
    return render(request, 'blog/sidebar.html', context)


class GetByCategory(ListView):
    template_name = 'blog/article_list.html'
    paginate_by = 4
    model = Article

    def get_queryset(self):
        category = self.kwargs['category_name']
        if category is not None:
            return Article.objects.filter(category__slug=category, status='p').all()
        else:
            return Article.objects.filter(status='p').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GetByCategory, self).get_context_data(**kwargs)
        context['setting'] = Setting.objects.last()
        return context


class GetByTag(ListView):
    template_name = 'blog/article_list.html'
    paginate_by = 4
    model = Article

    def get_queryset(self):
        tag = self.kwargs['tag_name']
        if tag is not None:
            return Article.objects.filter(tag__slug=tag, status='p').all()
        else:
            return Article.objects.filter(status='p').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GetByTag, self).get_context_data(**kwargs)
        context['setting'] = Setting.objects.last()
        return context


class Search(ListView):
    template_name = 'blog/article_list.html'
    paginate_by = 4
    model = Article

    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        if query is not None:
            return Article.objects.get_search(query=query)
        else:
            return Article.objects.filter(status='p').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['setting'] = Setting.objects.last()
        return context
