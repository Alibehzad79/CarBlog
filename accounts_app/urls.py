from django.urls import path

from accounts_app.views import dashboard, UserListView, delete_user_post, AdminListView, \
    add_remove_admin, active_de_active_user, UserBlockListView, create_new_user, edit_user_profile, \
    change_password_from_admin, edit_post, delete_skill, ArticleListView, category_list, category_edit, create_category, \
    article_filter, tag_list, create_tag, delete_tag, delete_category, tag_edit, create_article, delete_article, \
    article_gallery, gallery_list, remove_gallery, edit_article_gallery, seo_for_article_list, \
    delete_seo_for_article_list, create_seo_for_article_list, edit_seo_for_article_list, post_seo_list, \
    edit_article_seo, create_article_seo, delete_seo, suggestion_post_list, create_suggestion_post, \
    delete_suggestion_post, comment_list, edit_comment, delete_comment, sliders, edit_slider, login_view, delete_slider
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/create-new-user/', create_new_user, name='create-new-user'),
    path('dashboard/user-list/', UserListView.as_view(), name='user-list'),
    path('dashboard/admin-list/', AdminListView.as_view(), name='admin-list'),
    path('dashboard/block-list/', UserBlockListView.as_view(), name='block-list'),
    path('dashboard/edit-user/<int:pk>/delete-post/<int:post_id>/', delete_user_post, name='delete-user-post'),
    path('dashboard/edit-user/<int:user_id>/', edit_user_profile, name='edit-user'),
    path('dashboard/add-remove-admin/<int:user_id>/', add_remove_admin, name='add-remove-admin'),
    path('dashboard/active-deactive-user/<int:user_id>/', active_de_active_user, name='active-deactive-user'),
    path('login/', login_view, name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='registration/accounts/login.html'), name='logout'),
    path('change-password/<int:user_id>/', change_password_from_admin, name='change-password-from-admin'),
    path('edit-article/<int:post_id>/', edit_post, name='edit-article'),
    path('edit-user/delete-skill/<int:user_id>/<int:skill_id>/', delete_skill, name='delete-skill'),
    path('article-list/', ArticleListView.as_view(), name='article-list'),
    path('article-list/filter/<str:filter_name>/', article_filter, name='article-filter'),
    path('category-list/', category_list, name='category-list'),
    path('tag-list/', tag_list, name='tag-list'),
    path('category-edit/<int:category_id>/change/', category_edit, name='category-edit'),
    path('tag-edit/<int:tag_id>/change/', tag_edit, name='tag-edit'),
    path('create-category/new/', create_category, name='create-category'),
    path('create-tag/new/', create_tag, name='create-tag'),
    path('delete-tag/<int:tag_id>/', delete_tag, name='delete-tag'),
    path('delete-category/<int:category_id>/', delete_category, name='delete-category'),
    path('create-article/new/', create_article, name='create-article'),
    path('delete-article/<int:article_id>/', delete_article, name='delete-article'),
    path('gallery-list/', gallery_list, name='gallery-list'),
    path('create-gallery/', article_gallery, name='create-gallery'),
    path('remove-gallery/<int:gallery_id>/', remove_gallery, name='remove-gallery'),
    path('edit-gallery/<int:gallery_id>/', edit_article_gallery, name='edit-gallery'),
    path('seo-listArticle/', seo_for_article_list, name='seo-articleList'),
    path('delete-seo-listArticle/<int:seo_id>/', delete_seo_for_article_list, name='delete-seo-articleList'),
    path('edit-seo-listArticle/<int:seo_id>/', edit_seo_for_article_list, name='edit-seo-articleList'),
    path('create_seo_for_article_list/', create_seo_for_article_list, name='create_seo_for_article_list'),
    path('post-seo-list/', post_seo_list, name='post-seo-list'),
    path('edit-article-seo/<int:article_id>/', edit_article_seo, name='edit-article-seo'),
    path('create-article-seo/', create_article_seo, name='create-article-seo'),
    path('delete-seo/<int:seo_id>/', delete_seo, name='delete-seo'),
    path('suggestion-post-list/', suggestion_post_list, name='suggestion-post-list'),
    path('create-suggestion-post/', create_suggestion_post, name='create-suggestion-post'),
    path('delete-suggestion-post/<int:post_id>/', delete_suggestion_post, name='delete-suggestion-post'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete-comment'),
    path('comments/', comment_list, name='comments'),
    path('edit-comment/<int:comment_id>/', edit_comment, name='edit-comment'),
    path('sliders/', sliders, name='sliders'),
    path('sliders/edit/<int:slider_id>/', edit_slider, name='edit-slider'),
    path('delete-slider/<int:slider_id>/', delete_slider, name='delete-slider'),

]
