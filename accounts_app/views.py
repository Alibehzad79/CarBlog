import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.apps import apps
from pyparsing import make_xml_tags

from accounts_app.forms import CreateNewUserForm, EditUserProfileForm, ChangeUserPasswordForm, \
    EditArticleForm, CategoryEditFrom, CreateCategoryFrom, CreateTagFrom, TagEditFrom, ArticleForm, GalleryForm, \
    EditGalleryForm, CreateSeoArticleListForm, EditSeoArticleListForm, EditArticleSeo, CreateArticleSeo, \
    SuggestionPostForm, EditCommentForm
from accounts_app.models import CustomUser
from blog_app.models import Article, Category, Tag, ArticleGallery, SeoArticleList, Seo, SuggestionPost, ArticleComment
from django.contrib.auth.mixins import PermissionDenied
from django.forms import inlineformset_factory

from config import settings


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def dashboard(request):
    if request.user.is_superuser and request.user.is_staff:
        userModel = CustomUser.objects.all()
        user = request.user
        user.last_login = datetime.datetime.now()
        user.save()
        articleModel = Article.objects.all()
        visit_all = 0
        for article in Article.objects.all():
            visit_all += article.visit_count
        my_visit_posts = 0
        for article in Article.objects.filter(creator=request.user):
            my_visit_posts += article.visit_count
        context = {
            'userModel': userModel,
            'user': user,
            'articleModel': articleModel,
            'visit_all': visit_all,
            'my_visit_posts': my_visit_posts,
        }
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return redirect('login')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def dashboard_header(request):
    context = {
    }
    return render(request, 'dashboard/Header.html', context)


@login_required(login_url='/admin?next=accounts/dashboard/')
def dashboard_footer(request):
    context = {}
    return render(request, 'dashboard/Footer.html', context)


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def admin_sidebar(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'dashboard/sidebar.html', context)


class UserListView(ListView, PermissionDenied):
    model = CustomUser
    template_name = 'dashboard/user_list.html'
    paginate_by = 10
    login_required('/accounts/login?next=accounts/dashboard/')

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['user_path'] = self.request.path
        return context


class AdminListView(ListView):
    model = CustomUser
    template_name = 'dashboard/user_list.html'
    paginate_by = 10
    login_required('/accounts/login?next=accounts/dashboard/')

    def get_queryset(self):
        return CustomUser.objects.filter(is_superuser=True).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        context['admin_path'] = self.request.path
        return context


class UserBlockListView(ListView):
    model = CustomUser
    template_name = 'dashboard/user_list.html'
    paginate_by = 10
    login_required('/admin?next=accounts/dashboard/')

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=False).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserBlockListView, self).get_context_data(**kwargs)
        context['block_path'] = self.request.path
        return context


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_user_post(request, **kwargs):
    user = CustomUser.objects.get(id=request.user.id)
    if not request.user.is_superuser:
        return redirect('dashboard')
    post_id = kwargs['post_id']
    post = Article.objects.get(id=post_id)
    post.delete()
    return redirect('edit-user', user.id)


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def add_remove_admin(request, **kwargs):
    if request.user.is_superuser:
        user_id = kwargs['user_id']
        user = CustomUser.objects.get(id=user_id)
        if user.is_superuser:
            user.is_superuser = False
            user.is_staff = False
            user.is_active = True
            user.save()
        elif user.is_staff:
            user.is_superuser = True
            user.save()
        elif user.is_active:
            user.is_staff = True
            user.save()
        else:
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()
        return redirect('user-list')
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def active_de_active_user(request, **kwargs):
    if request.user.is_superuser:
        user_id = kwargs['user_id']
        user = CustomUser.objects.get(id=user_id)
        if user.is_active or user.is_superuser or user.is_staff:
            if user.is_superuser:
                user.is_active = False
                user.is_superuser = False
                user.is_staff = False
                user.save()
            else:
                user.is_active = False
                user.is_staff = False
                user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('user-list')
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def create_new_user(request):
    if request.user.is_superuser:
        form = CreateNewUserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            new_user = CustomUser.objects.create_user(username=username, password=password1)
            if new_user is not None:
                return redirect('user-list')
            form = CreateNewUserForm()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_new_user.html', context)
    else:
        return redirect('dashboard')


def convert_to_list(string):
    li = list(string.split(","))
    return li


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def edit_user_profile(request, **kwargs):
    if request.user.is_superuser:
        user_id = kwargs['user_id']
        user = CustomUser.objects.get(id=user_id)
        my_visit_posts = 0
        for article in Article.objects.filter(creator=user):
            my_visit_posts += article.visit_count
        skills = user.skill_set.all()
        skls = []
        for skl in skills:
            skls.append(skl.skill)
        if not skills:
            skills = ''

        if request.method == 'POST':
            form = EditUserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                if user.first_name:
                    if first_name == '':
                        first_name = user.first_name
                last_name = form.cleaned_data.get('last_name')
                if user.last_name:
                    if last_name == '':
                        last_name = user.last_name
                profile_image = form.cleaned_data.get('profile_image')
                if user.photo:
                    if profile_image == '':
                        profile_image = user.photo
                address = form.cleaned_data.get('address')
                if user.location:
                    if address == '':
                        address = user.location
                about_me = form.cleaned_data.get('about_me')
                if user.about_me:
                    if about_me == '':
                        about_me = user.about_me
                education = form.cleaned_data.get('education')
                if user.education:
                    if education == '':
                        education = user.education
                my_skill = form.cleaned_data.get('my_skill')
                my_skills = convert_to_list(my_skill)
                user.first_name, user.last_name, user.photo, user.education, user.location, user.about_me = first_name, last_name, profile_image, education, address, about_me
                skils = []
                for skil in skills:
                    skils.append(skil.skill)
                for skill in my_skills:
                    if skill in skils or skill == '':
                        continue
                    else:
                        user.skill_set.create(skill=skill)
                user.save()
                CustomUser.save(user)
                return redirect(request.path)
        else:
            initials = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_image': user.photo,
                'address': user.location,
                'about_me': user.about_me,
                'education': user.education,
                'my_skill': [s for s in skls],
            }
            form = EditUserProfileForm(initial=initials)
        context = {
            'form': form,
            'visit_count': my_visit_posts,
            'customuser': user,
            'path': request.path,
        }
        return render(request, 'dashboard/edit-user-detail.html', context)

    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def change_password_from_admin(request, **kwargs):
    if request.user.is_superuser:
        user_id = kwargs['user_id']
        user = CustomUser.objects.get(id=user_id)
        form = ChangeUserPasswordForm(request.POST or None)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            return redirect('dashboard')
        else:
            form = ChangeUserPasswordForm()

        context = {
            'form': form,
        }
        return render(request, 'dashboard/change_password_from_admin.html', context)
    else:
        return redirect('/')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def edit_post(request, **kwargs):
    if request.user.is_superuser:
        post_id = kwargs['post_id']
        article = Article.objects.filter(id=post_id).exists()
        if article:
            article = Article.objects.get(id=post_id)
            if request.method == 'POST':
                form = EditArticleForm(request.POST, request.FILES)
                if form.is_valid():
                    title = form.cleaned_data.get('title')
                    if article.title:
                        if title == '' or title is None:
                            title = article.title
                    content = form.cleaned_data.get('content')
                    if article.content:
                        if content == '' or content is None:
                            content = article.content
                    image = form.cleaned_data.get('image')
                    if article.image:
                        if image == '' or image is None:
                            image = article.image
                    video_url = form.cleaned_data.get('video_url')
                    if article.video_url:
                        if video_url == '' or video_url is None:
                            video_url = article.video_url
                    category = form.cleaned_data.get('category')
                    if article.category:
                        if category == '' or category is None:
                            category = article.category
                    tag = form.cleaned_data.get('tag')
                    if article.tag:
                        if tag == '' or tag is None:
                            tag = article.tag
                    status = form.cleaned_data.get('status')
                    if article.status:
                        if status == '' or status == 'n' or status is None:
                            status = article.status
                    article.title, article.content, article.image, article.video_url, article.category, \
                    article.status, article.date_update = title, content, image, video_url, category, status, datetime.datetime.now()
                    for t in tag.all():
                        if t in article.tag.all():
                            article.tag.remove(t)
                        else:
                            article.tag.add(t)
                    article.save()
                    Article.save(article)
                    return redirect('article-list')
            else:
                initials = {
                    'title': article.title,
                    'content': article.content,
                    'image': article.image,
                    'video_url': article.video_url,
                    'status': article.status,
                }
                form = EditArticleForm(initial=initials)
            context = {
                'form': form,
                'article': article,
            }
            return render(request, 'dashboard/edit-article.html', context)
        else:
            return redirect('dashboard')
    else:
        return redirect('/')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_skill(request, **kwargs):
    if request.user.is_superuser:
        user_id = kwargs['user_id']
    else:
        user_id = request.user.id
    skill_id = kwargs['skill_id']
    user = CustomUser.objects.get(id=user_id)
    user_skill = user.skill_set.filter(id=skill_id)
    if user_skill.exists():
        user_skill.delete()
        user.save()
        return redirect('edit-user', user_id)
    else:
        return redirect('dashboard')


class ArticleListView(ListView):
    template_name = 'dashboard/article-list.html'
    model = Article
    paginate_by = 10
    login_required(login_url='/accounts/login?next=accounts/dashboard/')

    def get_queryset(self):
        return Article.objects.order_by('-id').all()


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def category_list(request, **kwargs):
    if request.user.is_superuser:
        categories = Category.objects.order_by('-id').all()
        context = {
            'categories': categories,
        }
        return render(request, 'dashboard/category_list.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def tag_list(request, **kwargs):
    if request.user.is_superuser:
        tags = Tag.objects.order_by('-id').all()
        context = {
            'categories': tags,
        }
        return render(request, 'dashboard/category_list.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def category_edit(request, **kwargs):
    if request.user.is_superuser:
        category_id = kwargs['category_id']
        category = Category.objects.get(id=category_id)
        form = CategoryEditFrom(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            en_name = form.cleaned_data.get('en_name')
            slug = en_name.replace(' ', '-')
            category.name = name
            category.slug = slug
            category.save()
            Category.save(category)
            return redirect('category-list')
        else:
            form = CategoryEditFrom(initial={'name': category.name, 'en_name': category.slug})
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'dashboard/category_edit.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def tag_edit(request, **kwargs):
    if request.user.is_superuser:
        tag_id = kwargs['tag_id']
        tag = Tag.objects.get(id=tag_id)
        form = TagEditFrom(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            en_name = form.cleaned_data.get('en_name')
            slug = en_name.replace(' ', '-')
            tag.name = name
            tag.slug = slug
            tag.save()
            Tag.save(tag)
            return redirect('tag-list')
        else:
            form = TagEditFrom(initial={'name': tag.name, 'en_name': tag.slug})
        context = {
            'category': tag,
            'form': form,
        }
        return render(request, 'dashboard/tag_edit.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def create_category(request):
    if request.user.is_superuser:
        form = CreateCategoryFrom(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            en_name = form.cleaned_data.get('en_name')
            slug = en_name.replace(' ', '-')
            new_category = Category.objects.create(name=name, slug=slug)
            if new_category is not None:
                new_category.save()
                return redirect('category-list')
        else:
            form = CreateCategoryFrom()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_category.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def create_tag(request):
    if request.user.is_superuser:
        form = CreateTagFrom(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            en_name = form.cleaned_data.get('en_name')
            slug = en_name.replace(' ', '-')
            new_tag = Tag.objects.create(name=name, slug=slug)
            if new_tag is not None:
                new_tag.save()
                return redirect('tag-list')
        else:
            form = CreateTagFrom()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_category.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_category(request, **kwargs):
    category_id = kwargs['category_id']
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('category-list')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_tag(request, **kwargs):
    tag_id = kwargs['tag_id']
    tag = Tag.objects.get(id=tag_id)
    tag.delete()
    return redirect('tag-list')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def article_filter(request, **kwargs):
    filter_name = kwargs['filter_name']
    if filter_name == 'my-articles':
        article_list = Article.objects.filter(creator=request.user).all()
    else:
        article_list = Article.objects.order_by(filter_name).all()
    context = {
        'article_list': article_list,
    }
    return render(request, 'dashboard/article-list.html', context)


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def create_article(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('article-list')
        else:
            form = ArticleForm()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_article.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_article(request, **kwargs):
    if request.user.is_superuser:
        article_id = kwargs['article_id']
        article = Article.objects.filter(id=article_id).exists()
        if article:
            article = Article.objects.get(id=article_id)
            article.delete()
            return redirect('article-list')
        else:
            return redirect('article-list')
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def gallery_list(request):
    if request.user.is_superuser:
        context = {
            'galleries': ArticleGallery.objects.all(),
        }
        return render(request, 'dashboard/gallery_list.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def article_gallery(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = GalleryForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                alt = form.cleaned_data.get('alt')
                article = form.cleaned_data.get('article')
                get_article = Article.objects.get(id=article.id)
                get_article = ArticleGallery.objects.create(article=get_article, title=alt, image=image)
                if get_article is not None:
                    get_article.save()
                    return redirect('gallery-list')
        else:
            form = GalleryForm()
        context = {
            'form': form,
        }

        return render(request, 'dashboard/create_gallery.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def remove_gallery(request, **kwargs):
    if request.user.is_superuser:
        gallery_id = kwargs['gallery_id']
        gallery = ArticleGallery.objects.filter(id=gallery_id).exists()
        if gallery:
            ArticleGallery.objects.get(id=gallery_id).delete()
            return redirect('gallery-list')
        else:
            return redirect('gallery-list')

    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def edit_article_gallery(request, **kwargs):
    if request.user.is_superuser:
        gallery_id = kwargs['gallery_id']
        gallery = ArticleGallery.objects.get(id=gallery_id)
        if request.method == 'POST':
            form = EditGalleryForm(request.POST, request.FILES,
                                   initial={'alt': gallery.title, 'image': gallery.image,
                                            'article': gallery.article})
            if form.is_valid():
                image = form.cleaned_data.get('image')
                alt = form.cleaned_data.get('alt')
                article = form.cleaned_data.get('article')
                gallery_article = ArticleGallery.objects.get(id=gallery_id)
                gallery_article.article, gallery_article.title, gallery_article.image = article, alt, image
                gallery_article.save()
                ArticleGallery.save(gallery_article)
                return redirect('gallery-list')
        else:
            form = EditGalleryForm(initial={'gallery_id': gallery.id, 'alt': gallery.title, 'image': gallery.image,
                                            'article': gallery.article})
        context = {
            'form': form,
            'gallery': gallery,
        }

        return render(request, 'dashboard/gallery_edit.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def seo_for_article_list(request):
    if request.user.is_superuser:
        seos = SeoArticleList.objects.order_by('-id').all()
        context = {
            'seos': seos,
        }
        return render(request, 'dashboard/seo_list_for_article_list.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_seo_for_article_list(request, **kwargs):
    if request.user.is_superuser:
        seo_id = kwargs['seo_id']
        seos = SeoArticleList.objects.filter(id=seo_id).exists()
        if seos:
            SeoArticleList.objects.get(id=seo_id).delete()
            return redirect('seo-articleList')
        else:
            return redirect('dashboard')
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def create_seo_for_article_list(request):
    if request.user.is_superuser:
        form = CreateSeoArticleListForm(request.POST or None)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            keywords = form.cleaned_data.get('keywords')
            description = form.cleaned_data.get('description')
            new_seo = SeoArticleList.objects.create(title=title, keywords=keywords, description=description)
            if new_seo is not None:
                new_seo.save()
                return redirect('seo-articleList')
            else:
                form = CreateSeoArticleListForm()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_seo_for_articleList.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def edit_seo_for_article_list(request, **kwargs):
    if request.user.is_superuser:
        seo_id = kwargs['seo_id']
        seo = SeoArticleList.objects.filter(id=seo_id).exists()
        if seo:
            seo = SeoArticleList.objects.get(id=seo_id)
            if request.method == 'POST':
                form = EditSeoArticleListForm(request.POST or None)
                if form.is_valid():
                    title = form.cleaned_data.get('title')
                    keywords = form.cleaned_data.get('keywords')
                    description = form.cleaned_data.get('description')
                    seo.title, seo.keywords, seo.description = title, keywords, description
                    seo.save()
                    return redirect('seo-articleList')
            else:
                initials = {
                    'title': seo.title,
                    'keywords': seo.keywords,
                    'description': seo.description,
                }
                form = EditSeoArticleListForm(initial=initials)
            context = {
                'form': form,
                'seo': seo,
            }
            return render(request, 'dashboard/edit_seo_articleList.html', context)
        else:
            return redirect('seo-articleList')

    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def post_seo_list(request):
    if request.user.is_superuser:
        seos = Seo.objects.all()
        context = {
            'seos': seos,
        }
        return render(request, 'dashboard/post_seo_list.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def edit_article_seo(request, **kwargs):
    if request.user.is_superuser:
        article_id = kwargs['article_id']
        article = Article.objects.filter(id=article_id).exists()
        if article:
            article = Article.objects.get(id=article_id)
            seo = Seo.objects.get(article_id=article.id)
            if request.method == 'POST':
                form = EditArticleSeo(request.POST or None)
                if form.is_valid():
                    article_id = form.cleaned_data.get('article_id')
                    title = form.cleaned_data.get('title')
                    keywords = form.cleaned_data.get('keywords')
                    description = form.cleaned_data.get('description')
                    article = Article.objects.get(id=article_id)
                    seo.article, seo.title, seo.keywords, seo.description = article, title, keywords, description
                    seo.save()
                    return redirect('post-seo-list')
            else:
                initials = {
                    'article_id': seo.article.id,
                    'title': seo.title,
                    'keywords': seo.keywords,
                    'description': seo.description
                }
                form = EditArticleSeo(initial=initials)
            context = {
                'form': form,
                'article': article,
            }
            return render(request, 'dashboard/edit_article_seo.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def create_article_seo(request, **kwargs):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CreateArticleSeo(request.POST or None)
            if form.is_valid():
                article = form.cleaned_data.get('article')
                title = form.cleaned_data.get('title')
                keywords = form.cleaned_data.get('keywords')
                description = form.cleaned_data.get('description')
                if Seo.objects.filter(article=article).exists():
                    return HttpResponse(
                        '<h1>قبلا برای این پست سئو تعریف شده<h1><a href="/accounts/post-seo-list/">برگشت</a>')
                new_seo = Seo.objects.create(article=article, title=title, keywords=keywords, description=description)
                if new_seo is not None:
                    new_seo.save()
                    return redirect('post-seo-list')
        else:
            form = CreateArticleSeo()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_article_seo.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_seo(request, **kwargs):
    if request.user.is_superuser:
        seo_id = kwargs['seo_id']
        if Seo.objects.filter(id=seo_id).exists():
            Seo.objects.get(id=seo_id).delete()
            return redirect('post-seo-list')
        else:
            return redirect('dashboard')
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def suggestion_post_list(request):
    if request.user.is_superuser:
        suggestion_post = SuggestionPost.objects.all()
        context = {
            'suggestion_post_list': suggestion_post,
        }
        return render(request, 'dashboard/suggestion_post.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def create_suggestion_post(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SuggestionPostForm(request.POST or None)
            if form.is_valid():
                post = form.cleaned_data.get('post')
                if SuggestionPost.objects.filter(article=post).exists():
                    return HttpResponse(
                        '<a dir="rtl" style="padding:10px;color: white;background-color:blue;" '
                        'href="/accounts/suggestion-post-list/">بازگشت</a> قبلا انتخاب شده')
                new_suggestion = SuggestionPost.objects.create(article=post)
                if new_suggestion is not None:
                    return redirect('suggestion-post-list')
        else:
            form = SuggestionPostForm()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_suggestion_post.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_suggestion_post(request, **kwargs):
    if request.user.is_superuser:
        post_id = kwargs['post_id']
        if SuggestionPost.objects.filter(article_id=post_id).exists():
            SuggestionPost.objects.filter(article_id=post_id).delete()
            return redirect('suggestion-post-list')
        else:
            return HttpResponse('پست مورد نظر یافت نشد')
    else:
        return redirect('dashboard')


# todo create comment list page and create edit page for this page
@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def comment_list(request):
    if request.user.is_superuser:
        comments = ArticleComment.objects.all()
        context = {
            'comments': comments,
        }
        return render(request, 'dashboard/comment_list.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def edit_comment(request, **kwargs):
    if request.user.is_superuser:
        comment_id = kwargs['comment_id']
        comment = ArticleComment.objects.filter(id=comment_id).exists()
        if comment:
            comment = ArticleComment.objects.get(id=comment_id)
            if request.method == 'POST':
                form = EditCommentForm(request.POST or None)
                if form.is_valid():
                    post = form.cleaned_data.get('post')
                    name = form.cleaned_data.get('name')
                    email = form.cleaned_data.get('email')
                    text = form.cleaned_data.get('comment')
                    status = form.cleaned_data.get('status')
                    comment.article, comment.name, comment.email, comment.text, comment.status = post, name, email, text, status
                    comment.save()
                    return redirect('comments')
            else:
                initials = {
                    'post': comment.article,
                    'name': comment.name,
                    'email': comment.email,
                    'comment': comment.text,
                    'status': comment.status,
                }
                form = EditCommentForm(initial=initials)
            context = {
                'form': form,
                'comment': comment,
            }
            return render(request, 'dashboard/edit_comment.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='/accounts/login?next=accounts/dashboard/')
def delete_comment(request, **kwargs):
    if request.user.is_superuser:
        comment_id = kwargs['comment_id']
        if ArticleComment.objects.filter(id=comment_id).exists():
            ArticleComment.objects.filter(id=comment_id).delete()
            return redirect('comments')
        else:
            return HttpResponse('نظر مورد نظر یافت نشد')
    else:
        return redirect('dashboard')
