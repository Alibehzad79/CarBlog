from django.contrib import admin

# Register your models here.
from slider_app.models import Slider


@admin.action(description='منتشر کردن')
def get_published(modeladmin, request, queryset):
    queryset.update(status='p')


@admin.action(description='منتشر نکردن')
def get_unpublished(modeladmin, request, queryset):
    queryset.update(status='u')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    list_editable = ('status',)
    search_fields = ('title', 'url')
    actions = [get_published, get_unpublished]
