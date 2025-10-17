from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('thanks/', views.thanks, name='thanks'),
    path('projects/ajax-add/', views.ajax_add_project, name='ajax_add_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/', views.projects_list, name='projects_list'),
]
