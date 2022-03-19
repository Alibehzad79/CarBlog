from django.contrib import admin

# Register your models here.
from site_settings_app.models import Setting, Phone, Email, Address, SocialNetwork, SeoHomePage


class PhoneTabularInline(admin.TabularInline):
    model = Phone


class EmailTabularInline(admin.TabularInline):
    model = Email


class AddressTabularInline(admin.TabularInline):
    model = Address


class SocialNetworkTabularInline(admin.TabularInline):
    model = SocialNetwork


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    inlines = [PhoneTabularInline, EmailTabularInline, AddressTabularInline, SocialNetworkTabularInline]


admin.site.register(SeoHomePage)
