# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import logging
from .models import Service, Project, TeamMember
from .forms import ContactForm

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    try:
        services = Service.objects.filter(is_active=True).order_by('order')[:6]
        projects = Project.objects.filter(published=True).order_by('order')[:6]
        team = TeamMember.objects.filter(is_active=True).order_by('order')[:6]
        form = ContactForm()

        context = {
            'services': services,
            'projects': projects,
            'team': team,
            'form': form,
        }
        return render(request, 'index.html', context)

    except Exception as e:
        logger.error(f"Error in index view: {str(e)}", exc_info=True)
        messages.error(request, 'خطایی در بارگذاری صفحه رخ داده است.')
        return render(request, 'index.html', {
            'services': [],
            'projects': [],
            'team': [],
            'form': ContactForm(),
        })


def contact_submit(request):
    return render(request, 'partials/_contact.html')


def thanks(request):
    """صفحه تشکر پس از ارسال فرم"""
    return render(request, 'partials/thanks.html')


def project_detail(request):
    """صفحه تشکر پس از ارسال فرم"""
    return render(request, 'partials/_project_detail.html')
