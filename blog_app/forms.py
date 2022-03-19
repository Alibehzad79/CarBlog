from django import forms
from django.core import validators

from blog_app.models import ArticleComment


class ArticleCommentForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": 'آدرس ایمیل'}),
        validators=[
            validators.EmailValidator
        ]
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": 'نام و نام خانوادگی'}),
        validators=[
            validators.MaxLengthValidator(25, 'طول نام و نام خانوادگی نباید بیشتر از 25 کلمه باشد.'),
            validators.MinLengthValidator(3, 'طول نام و نام خانوادگی نباید کمتر از 3 کلمه باشد.')
        ]
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": 'پیغام...'}),
    )

    article_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
