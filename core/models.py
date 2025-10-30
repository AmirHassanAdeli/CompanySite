# core/models.py
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    icon = models.CharField(max_length=100, verbose_name="آیکون", help_text="کلاس Font Awesome")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس‌ها"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان پروژه")
    description = models.TextField(verbose_name="توضیحات")
    short_description = models.CharField(max_length=300, verbose_name="توضیح کوتاه", blank=True)
    technologies = models.CharField(max_length=500, verbose_name="تکنولوژی‌ها", help_text="با کاما جدا کنید")
    icon = models.CharField(max_length=100, verbose_name="آیکون", default='fas fa-cog',
                            help_text="کلاس Font Awesome")
    demo_url = models.URLField(verbose_name="آدرس دمو", blank=True)
    github_url = models.URLField(verbose_name="آدرس گیت‌هاب", blank=True)
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    position = models.CharField(max_length=100, verbose_name="سمت")
    bio = models.TextField(verbose_name="بیوگرافی")
    image = models.ImageField(upload_to='team/', verbose_name="تصویر")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} - {self.position}"


class Contact(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی", validators=[MinLengthValidator(2)])
    phone = models.CharField(max_length=15, verbose_name="تلفن")
    message = models.TextField(verbose_name="پیام", validators=[MinLengthValidator(5)])
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ارسال")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.phone}"
