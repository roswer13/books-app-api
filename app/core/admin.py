"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import User, Page, Book


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'role', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    search_fields = ['email', 'name']
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'name', 'role',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )


class PageInline(admin.TabularInline):
    """Inline for pages in the book admin."""
    model = Page
    extra = 0
    fields = ["number", "content"]
    readonly_fields = ["number",]
    show_change_link = True
    ordering = ["number"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Define the admin pages for books."""
    list_display = ['title', 'author']
    search_fields = ['title', 'author']
    inlines = [PageInline]

    readonly_fields = ['created_at', 'updated_at', 'uuid']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Define the admin pages for pages."""
    list_display = ['uuid', 'book', 'number']
    search_fields = ['book__title']
    readonly_fields = ['uuid',]
