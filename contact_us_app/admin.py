from django.contrib import admin

# Register your models here.
from contact_us_app.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'email', 'subject', 'date_send')
    list_filter = ('date_send',)
    search_fields = ('name', 'email', 'subject', 'message')
