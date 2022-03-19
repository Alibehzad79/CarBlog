from django.contrib import admin

# Register your models here.
from aboutUs_app.models import AboutUs, Team


class TeamTabularInline(admin.TabularInline):
    model = Team


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = [TeamTabularInline]
