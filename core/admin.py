from django.contrib import admin
from .models import Service, Project, TeamMember, Contact


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


@admin.register(Contact)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email']
    search_fields = ['first_name', 'last_name', 'phone', 'email']

