from django.urls import path

from contact_us_app.views import contact_us

app_name = 'contact'
urlpatterns = [
    path('', contact_us, name='contact-us'),
]
