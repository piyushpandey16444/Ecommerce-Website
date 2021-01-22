from django.core.exceptions import ValidationError
from django.contrib import messages

from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import *


class BusinessorderAdmin(admin.ModelAdmin):
    list_display = ('id', 'businessorder_name', 'businessorder_url',)
    list_display_links = ('id', 'businessorder_name')

    def has_delete_permission(self, request, obj=None):
        return False


# admin.site.register(Businessorder, BusinessorderAdmin)