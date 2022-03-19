import datetime

from django.shortcuts import render, redirect

from blog_app.models import Article, SuggestionPost
from site_settings_app.models import Setting, SeoHomePage
from slider_app.models import Slider
from subscribe_app.forms import SubscribeForm
from subscribe_app.models import Subscribe


def header(request):
    context = {}
    return render(request, 'Base/Header.html', context)


def home_page(request):
    setting = Setting.objects.last()
    articles = Article.objects.filter(status='p').order_by('-id').all()[:8]
    suggestion_posts = SuggestionPost.objects.filter(article__status='p').order_by('-id').all()[:3]
    meta_tag = SeoHomePage.objects.last()
    sliders = Slider.objects.filter(status='p').order_by('-id').all()

    context = {
        'articles': articles,
        'suggestion_posts': suggestion_posts,
        'setting': setting,
        'meta_tag': meta_tag,
        'sliders': sliders,
    }
    return render(request, 'index.html', context)


def footer(request):
    now_year = datetime.datetime.now()
    setting = Setting.objects.last()
    form = SubscribeForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')

        new_subscribe = Subscribe.objects.create(email=email, date_send=datetime.datetime.now())
        if new_subscribe is not None:
            new_subscribe.save()
        form = SubscribeForm()
    context = {
        'now_year': now_year,
        'setting': setting,
        'form': form,
    }
    return render(request, 'Base/Footer.html', context)


def base(request):
    setting = Setting.objects.last()
    context = {
        'setting': setting,
    }
    return render(request, 'Base/base.html', context)
