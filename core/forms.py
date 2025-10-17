# forms.py
from django import forms
from .models import ContactMessage, Project
import re


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'company', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شرکت (اختیاری)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس (اختیاری)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع پیام (اختیاری)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام شما...',
                'rows': 5,
                'required': True
            }),
        }
        labels = {
            'name': 'نام کامل',
            'email': 'آدرس ایمیل',
            'company': 'شرکت',
            'phone': 'شماره تماس',
            'subject': 'موضوع',
            'message': 'پیام',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # اعتبارسنجی شماره تلفن ایرانی
            phone_pattern = r'^(\+98|0)?9\d{9}$'
            if not re.match(phone_pattern, phone.replace(' ', '')):
                raise forms.ValidationError('لطفاً شماره تلفن معتبر وارد کنید')
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError('نام باید حداقل ۲ حرف باشد')
        return name.strip()

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError('پیام باید حداقل ۱۰ حرف باشد')
        return message.strip()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'icon', 'color', 'category', 'demo_url', 'github_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان پروژه',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات کامل پروژه...',
                'rows': 4,
                'required': True
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'JavaScript, React, Python, Django...'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-code'
            }),
            'color': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'demo_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repo'
            }),
        }
        labels = {
            'title': 'عنوان پروژه',
            'description': 'توضیحات',
            'technologies': 'تکنولوژی‌ها',
            'icon': 'آیکون',
            'color': 'رنگ پس‌زمینه',
            'category': 'دسته‌بندی',
            'demo_url': 'آدرس دمو',
            'github_url': 'آدرس گیت‌هاب',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن گزینه‌های رنگ به صورت داینامیک
        self.fields['color'].widget = forms.Select(choices=[
            ('linear-gradient(135deg, #00d4ff 0%, #6a5acd 50%, #c0c0c0 100%)', 'آبی فیروزه‌ای-بنفش-نقره‌ای'),
            ('linear-gradient(135deg, #00d4ff 20%, #6a5acd 80%)', 'آبی فیروزه‌ای-بنفش'),
            ('linear-gradient(135deg, #6a5acd 0%, #c0c0c0 60%, #00d4ff 100%)', 'بنفش-نقره‌ای-آبی'),
            ('linear-gradient(135deg, #c0c0c0 0%, #00d4ff 50%, #6a5acd 100%)', 'نقره‌ای-آبی-بنفش'),
        ], attrs={'class': 'form-control'})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 3:
            raise forms.ValidationError('عنوان پروژه باید حداقل ۳ حرف باشد')
        return title.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description.strip()) < 10:
            raise forms.ValidationError('توضیحات باید حداقل ۱۰ حرف باشد')
        return description.strip()

    def clean_technologies(self):
        technologies = self.cleaned_data.get('technologies')
        if technologies:
            tech_list = [tech.strip() for tech in technologies.split(',') if tech.strip()]
            if len(tech_list) == 0:
                raise forms.ValidationError('حداقل یک تکنولوژی وارد کنید')
        return technologies
