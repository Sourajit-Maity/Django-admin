from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class NoDeleteAdminMixin:
    def has_delete_permission(self, request, obj=None):
        #return False # Disable Delete
        return True   # Enable Delete

# ===================================================
# class Usage_log
# ===================================================
class Usage_log(NoDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('task_type', 'task_details', 'file_name', 'used_by','used_on')
    list_filter = ('task_type', 'used_by')
    search_fields = ('task_type', 'used_by')
    readonly_fields = ['used_by', 'used_on']
    def save_model(self, request, obj, form, change):
         # Custom function on save
         obj.used_by = request.user
         # Now call default save
         obj.save()
admin.site.register(usage_log,Usage_log)

# ===================================================
#   User profile extension
# ===================================================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

    # list_display = ('fullName', 'userType', 'designation')
    # list_filter = ('device_config__name', 'active', 'added_by')
    # readonly_fields = ['details', 'added_by', 'added_on']

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# ===================================================