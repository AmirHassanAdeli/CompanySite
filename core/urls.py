from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('project_detail/', views.project_detail, name='project_detail'),
    path('thanks/', views.thanks, name='thanks'),
]
