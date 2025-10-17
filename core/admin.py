from django.contrib import admin
from .models import Service, Project, TeamMember, ContactMessage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'featured', 'order', 'created_at']
    list_filter = ['category', 'published', 'featured', 'created_at']
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['published', 'featured', 'order']
    ordering = ['order', '-created_at']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'position', 'created_at']
    search_fields = ['name', 'position', 'bio']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent']

    def mark_as_read(self, request, queryset):
        queryset.update(status='read')

    mark_as_read.short_description = 'علامت‌گذاری به عنوان خوانده شده'

    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied')

    mark_as_replied.short_description = 'علامت‌گذاری به عنوان پاسخ داده شده'

    actions = [mark_as_read, mark_as_replied]
