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
from .models import Service, Project, TeamMember, ContactMessage
from .forms import ContactForm, ProjectForm

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


@require_http_methods(["POST"])
def contact_submit(request):
    form = ContactForm(request.POST)

    if form.is_valid():
        contact = form.save(commit=False)

        # ذخیره اطلاعات درخواست
        contact.ip_address = get_client_ip(request)
        contact.user_agent = request.META.get('HTTP_USER_AGENT', '')
        contact.save()

        try:
            # ارسال ایمیل
            subject = f"پیام جدید از {contact.name} - {contact.subject or 'بدون موضوع'}"

            body = f"""
نام: {contact.name}
ایمیل: {contact.email}
شرکت: {contact.company or 'ثبت نشده'}
تلفن: {contact.phone or 'ثبت نشده'}
IP: {contact.ip_address}

پیام:
{contact.message}

زمان ارسال: {contact.created_at.strftime('%Y-%m-%d %H:%M')}
            """.strip()

            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECEIVER],
                fail_silently=False,
            )

            logger.info(f"ایمیل تماس جدید از {contact.email} ارسال شد - Message ID: {contact.id}")
            messages.success(request, 'پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.')

        except Exception as e:
            logger.error(f"خطا در ارسال ایمیل برای {contact.email}: {str(e)}")
            messages.warning(request, 'پیام شما ذخیره شد، اما در ارسال ایمیل مشکلی پیش آمد.')

        return redirect(reverse('core:thanks'))

    else:
        # لاگ خطاهای فرم
        logger.warning(f"فرم تماس نامعتبر: {form.errors}")

        # نمایش خطاها به کاربر
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{form.fields[field].label}: {error}")

        return redirect(reverse('core:index') + '#contact')


def thanks(request):
    """صفحه تشکر پس از ارسال فرم"""
    return render(request, 'partials/thanks.html')


@csrf_exempt
@require_http_methods(["POST"])
def ajax_add_project(request):
    """ویو مخصوص AJAX برای اضافه کردن پروژه"""
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'})

    form = ProjectForm(request.POST)

    if form.is_valid():
        try:
            project = form.save(commit=False)

            # برای کاربران عادی، پروژه به صورت پیش‌نویس ذخیره شود
            if not request.user.is_authenticated or not request.user.is_staff:
                project.published = False

            project.save()

            logger.info(f"پروژه جدید از طریق AJAX اضافه شد: {project.title}")

            return JsonResponse({
                'success': True,
                'message': 'پروژه با موفقیت اضافه شد!',
                'project': {
                    'id': project.id,
                    'title': project.title,
                    'technologies': project.get_technologies_list(),
                    'icon': project.icon,
                    'color': project.color,
                    'description': project.description
                }
            })

        except Exception as e:
            logger.error(f"خطا در ذخیره پروژه AJAX: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'خطا در ذخیره پروژه'
            })

    else:
        errors = {}
        for field, field_errors in form.errors.items():
            errors[field] = field_errors[0] if field_errors else ''

        return JsonResponse({
            'success': False,
            'errors': errors
        })


@login_required
def project_list(request):
    """لیست پروژه‌ها برای مدیریت"""
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'admin/project_list.html', {'projects': projects})


@login_required
def toggle_project_publish(request, project_id):
    """تغییر وضعیت انتشار پروژه"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        project = get_object_or_404(Project, id=project_id)
        project.published = not project.published
        project.save()

        status = "منتشر شد" if project.published else "پیش‌نویس"

        return JsonResponse({
            'success': True,
            'published': project.published,
            'message': f'پروژه "{project.title}" {status}'
        })

    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'})


def project_detail(request, project_id):
    """صفحه جزئیات پروژه"""
    project = get_object_or_404(Project, id=project_id, published=True)
    return render(request, 'projects/detail.html', {'project': project})


def projects_list(request):
    """لیست تمام پروژه‌ها"""
    projects = Project.objects.filter(published=True).order_by('order', '-created_at')
    return render(request, 'projects/list.html', {'projects': projects})
