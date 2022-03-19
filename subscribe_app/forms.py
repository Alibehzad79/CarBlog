from django import forms
from django.core import validators


class SubscribeForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'ایمیل خود را وارد کنید...', 'class': 'email', 'name': 'EMAIL'}),
        validators=[
            validators.EmailValidator()
        ]
    )
