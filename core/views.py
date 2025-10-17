from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import logging
from .models import Service, Project, TeamMember, ContactMessage
from .forms import ContactForm

logger = logging.getLogger(__name__)


def index(request):
    try:
        services = Service.objects.all()
        projects = Project.objects.filter(published=True).order_by('order')[:6]
        team = TeamMember.objects.all()[:6]
        form = ContactForm()

        return render(request, 'index.html', {
            'services': services,
            'projects': projects,
            'team': team,
            'form': form,
        })
    except Exception as e:
        logger.error(f"Error in index view: {str(e)}")
        return render(request, 'index.html', {
            'services': [],
            'projects': [],
            'team': [],
            'form': ContactForm(),
        })


def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            try:
                subject = f"پیام جدید از {contact.name}"
                body = f"""
نام: {contact.name}
ایمیل: {contact.email}
شرکت: {contact.company or 'ثبت نشده'}

پیام:
{contact.message}

زمان ارسال: {contact.created_at.strftime('%Y-%m-%d %H:%M')}
                """.strip()

                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_RECEIVER]
                )
                logger.info(f"ایمیل تماس جدید از {contact.email} ارسال شد")
                messages.success(request, 'پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.')

            except Exception as e:
                logger.error(f"خطا در ارسال ایمیل برای {contact.email}: {str(e)}")
                messages.warning(request, 'پیام شما ذخیره شد، اما در ارسال ایمیل مشکلی پیش آمد.')

            return redirect(reverse('core:thanks'))
        else:
            logger.warning(f"فرم تماس نامعتبر: {form.errors}")
            messages.error(request, 'لطفاً اطلاعات فرم را به درستی تکمیل کنید.')

    return redirect(reverse('core:index'))


def thanks(request):
    return render(request, 'partials/thanks.html')
