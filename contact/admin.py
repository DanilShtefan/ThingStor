from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created']
    list_filter = ['is_read', 'subject', 'created']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created']
