from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'company', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شرکت (اختیاری)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'پیام شما...',
                'rows': 6
            }),
        }
        labels = {
            'name': 'نام کامل',
            'email': 'آدرس ایمیل',
            'company': 'شرکت',
            'message': 'پیام'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
            domain = email.split('@')[-1] if '@' in email else ''
            if domain.lower() not in allowed_domains:
                raise forms.ValidationError(
                    "لطفاً از یک سرویس ایمیل معتبر مانند Gmail، Yahoo یا Outlook استفاده کنید."
                )
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError("نام باید حداقل ۲ کاراکتر باشد.")
        return name.strip()

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError("پیام باید حداقل ۱۰ کاراکتر باشد.")
        return message.strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['message'].required = True
        self.fields['company'].required = False
