# core/views.py
import re
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import Service, Project, TeamMember, Contact

logger = logging.getLogger(__name__)


def index(request):
    services = Service.objects.all()
    projects = Project.objects.all()
    team = TeamMember.objects.all()

    context = {
        'services': services,
        'projects': projects,
        'team': team,
    }
    return render(request, 'index.html', context)


@require_POST
@csrf_protect
def contact_view(request):
    try:
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip().replace(' ', '')
        message = request.POST.get('message', '').strip()

        errors = {}

        if not name or len(name) < 2:
            errors['name'] = 'نام باید حداقل ۲ کاراکتر باشد.'
        if not phone or not re.match(r'^09[0-9]{9}$', phone):
            errors['phone'] = 'شماره تلفن معتبر نیست (مثال: 09123456789)'
        if not message or len(message) < 5:
            errors['message'] = 'پیام باید حداقل ۵ کاراکتر باشد.'

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        Contact.objects.create(full_name=name, phone=phone, message=message)
        logger.info(f"New contact: {name} - {phone}")

        return JsonResponse({
            'success': True,
            'message': 'پیام شما با موفقیت ارسال شد. در اسرع وقت با شما تماس می‌گیریم.'
        })

    except Exception as e:
        logger.error(f"Contact error: {e}")
        return JsonResponse({
            'success': False,
            'errors': {'general': ['خطای سرور رخ داد.']}
        }, status=500)
