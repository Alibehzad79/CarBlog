from django.shortcuts import render

# Create your views here.
from aboutUs_app.models import AboutUs
from site_settings_app.models import Setting


def about_us(request):
    about = AboutUs.objects.last()
    setting = Setting.objects.last()
    context = {
        "about": about,
        "setting": setting,
    }
    return render(request, 'about_us/about.html', context)
