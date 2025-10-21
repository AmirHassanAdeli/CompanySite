from django.contrib import admin
from .models import Service, Project, TeamMember, Contact


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', ]
    search_fields = ['title', 'description']
    list_editable = ['order', ]
    ordering = ['order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', ]
    list_filter = ['category', ]
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['order']
    ordering = ['order', ]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order']
    list_filter = ['position', ]
    search_fields = ['name', 'position', 'bio']
    list_editable = ['order', ]
    ordering = ['order']


@admin.register(Contact)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
