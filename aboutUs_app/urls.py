from django.urls import path
from aboutUs_app.views import about_us

app_name = 'about'
urlpatterns = [
    path('', about_us, name='about-us'),
]
