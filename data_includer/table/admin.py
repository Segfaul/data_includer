from django.contrib import admin

from .models import *


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'description', 'upload_date', 'modified_date', 'user')
    list_display_links = ('id', 'file', 'user')
    search_fields = ('file', 'description')
    list_filter = ('upload_date',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_staff', 'date_joined', 'api_token')
    list_display_links = ('id', 'username')
    search_fields = ('username',)
    list_filter = ('date_joined',)


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(User, UserAdmin)
