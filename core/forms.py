# forms.py
from django import forms
from .models import Contact, Project
import re


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
                'required': True
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی',
                'required': True
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس',
                'required': True
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما',
                'required': True
            }),
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone': 'شماره تماس',
            'email': 'آدرس ایمیل',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # اعتبارسنجی شماره تلفن ایرانی
            phone_pattern = r'^(\+98|0)?9\d{9}$'
            if not re.match(phone_pattern, phone.replace(' ', '')):
                raise forms.ValidationError('لطفاً شماره تلفن معتبر وارد کنید')
        return phone

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if len(name.strip()) < 2:
            raise forms.ValidationError('نام باید حداقل ۲ حرف باشد')
        return name.strip()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'icon', 'category', 'demo_url', 'github_url']

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
                'placeholder': 'JavaScript, React, Python, Django...',
                'required': True
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-code',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
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
            'category': 'دسته‌بندی',
            'demo_url': 'آدرس دمو',
            'github_url': 'آدرس گیت‌هاب',
        }

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
