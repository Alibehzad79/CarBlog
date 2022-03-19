from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts_app.models import CustomUser, Skill


@admin.action(description='برداشتن بن کاربر')
def on_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='بن کردن کاربر')
def off_active(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='ارتقا به ادمین پایین رده کاربر')
def on_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)


@admin.action(description='سلب امتیاز ادمین کاربر')
def off_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)


@admin.action(description='ارتقا به ابر کاربر')
def upto_superuser(modeladmin, request, queryset):
    queryset.update(is_superuser=True)


@admin.action(description='سلب امتیاز ابر کاربر')
def down_to_superuser(modeladmin, request, queryset):
    queryset.update(is_superuser=False)


class SkillAdminTabularInline(admin.TabularInline):
    model = Skill


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'photo', 'education', 'location', 'about_me')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    inlines = [SkillAdminTabularInline]
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('get_photo', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    actions = [on_active, off_active, on_staff, off_staff, upto_superuser, down_to_superuser]


CustomUser.get_photo.short_description = 'تصویر'
