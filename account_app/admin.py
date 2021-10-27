
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from . import models, forms

admin.site.site_title = 'Authentication Application'
admin.site.site_header = 'Authentication & Authorization Application'


class UserAdmin(BaseUserAdmin):
    """
    Admin Panel's User list and detail view
    """
    add_form = forms.UserSignupForm
    form = forms.UserUpdateAdminForm

    list_display = ('email', 'id', 'full_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff',)
    list_editable = ('is_active', 'is_staff')
    fieldsets = (
        ('Authentication Fields', {'fields': ('email', 'full_name', 'password',)}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('is_staff','is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone')
    ordering = ('-email',)
    filter_horizontal = ()


admin.site.register(models.UserBase, UserAdmin)
admin.site.unregister(Group)
