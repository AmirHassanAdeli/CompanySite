# views.py
from django.shortcuts import render
from django.contrib import messages
import logging
from .models import Service, Project, TeamMember
from .forms import ContactForm

logger = logging.getLogger(__name__)


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
