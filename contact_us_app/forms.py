from django import forms
from django.core import validators


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "نام و نام خانوادگی *"}),
        validators=[
            validators.MaxLengthValidator(25, 'تعداد کلمات نام و نام خانوادگی شما نباید بیشتر از 25 کلمه باشد'),
            validators.MinLengthValidator(3, 'تعداد کلمات نام و نام خانوادگی شما نباید کمتر از 3 کلمه باشد'),
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل *'}),
        validators=[
            validators.EmailValidator()
        ]
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "عنوان تماس *"}),
        validators=[
            validators.MaxLengthValidator(40, 'تعداد کلمات عنوان تماس نباید بیشتر از 40  کلمه باشد'),
            validators.MinLengthValidator(3, 'تعداد کلمات عنوان تماس نباید کمتر از 3 کلمه باشد'),
        ]
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "پیغام *"}),
    )
