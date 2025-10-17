from django.contrib import admin
from .models import Service, Project, ContactInfo, TeamMember, ContactMessage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'short_desc']
    list_editable = ['order']

    def short_desc(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description

    short_desc.short_description = 'توضیح کوتاه'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'published', 'created_at']
    list_editable = ['order', 'published']
    list_filter = ['published']
    readonly_fields = ['created_at']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow only one instance
        return not ContactInfo.objects.exists()


@admin.register(TeamMember)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'processed']
    list_filter = ['processed']
    readonly_fields = ['name', 'email', 'company', 'message', 'created_at']
    list_editable = ['processed']

    def has_add_permission(self, request):
        return False
