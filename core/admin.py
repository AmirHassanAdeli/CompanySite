# core/admin.py
from django.contrib import admin
from .models import Service, Project, TeamMember, Contact


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'demo_url')
    list_editable = ('order',)
    search_fields = ('title', 'technologies')
    filter_horizontal = ()


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'position')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'phone', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "علامت‌گذاری به عنوان خوانده شده"