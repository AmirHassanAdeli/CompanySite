# models.py
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    icon = models.CharField(max_length=100, verbose_name="آیکون", help_text="کلاس Font Awesome")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس‌ها"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Project(models.Model):
    PROJECT_CATEGORIES = [
        ('web', 'وب‌سایت'),
        ('mobile', 'موبایل'),
        ('ai', 'هوش مصنوعی'),
        ('desktop', 'دسکتاپ'),
        ('other', 'سایر'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان پروژه")
    description = models.TextField(verbose_name="توضیحات")
    short_description = models.CharField(max_length=300, verbose_name="توضیح کوتاه", blank=True)
    technologies = models.CharField(max_length=500, verbose_name="تکنولوژی‌ها", help_text="با کاما جدا کنید")
    category = models.CharField(max_length=20, choices=PROJECT_CATEGORIES, default='web')
    icon = models.CharField(max_length=100, verbose_name="آیکون", default='fas fa-cog',
                            help_text="کلاس Font Awesome")
    color = models.CharField(max_length=200, verbose_name="رنگ پس‌زمینه",
                             default='linear-gradient(135deg, #00d4ff 0%, #6a5acd 50%, #c0c0c0 100%)')
    demo_url = models.URLField(verbose_name="آدرس دمو", blank=True)
    github_url = models.URLField(verbose_name="آدرس گیت‌هاب", blank=True)
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    published = models.BooleanField(default=False, verbose_name="منتشر شده")
    featured = models.BooleanField(default=False, verbose_name="ویژه")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        """تبدیل رشته تکنولوژی‌ها به لیست"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    position = models.CharField(max_length=100, verbose_name="سمت")
    bio = models.TextField(verbose_name="بیوگرافی")
    image = models.ImageField(upload_to='team/', verbose_name="تصویر")
    email = models.EmailField(verbose_name="ایمیل", blank=True)
    phone = models.CharField(max_length=15, verbose_name="تلفن", blank=True)
    linkedin_url = models.URLField(verbose_name="لینکدین", blank=True)
    github_url = models.URLField(verbose_name="گیت‌هاب", blank=True)
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} - {self.position}"


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('read', 'خوانده شده'),
        ('replied', 'پاسخ داده شده'),
        ('spam', 'اسپم'),
    ]

    name = models.CharField(max_length=100, verbose_name="نام", validators=[MinLengthValidator(2)])
    email = models.EmailField(verbose_name="ایمیل")
    company = models.CharField(max_length=100, verbose_name="شرکت", blank=True)
    phone = models.CharField(max_length=15, verbose_name="تلفن", blank=True)
    subject = models.CharField(max_length=200, verbose_name="موضوع", blank=True)
    message = models.TextField(verbose_name="پیام", validators=[MinLengthValidator(10)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(verbose_name="آدرس IP", null=True, blank=True)
    user_agent = models.TextField(verbose_name="User Agent", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"

    def mark_as_read(self):
        self.status = 'read'
        self.save()

    def mark_as_replied(self):
        self.status = 'replied'
        self.save()


class ContactInfo(models.Model):
    CONTACT_TYPES = [
        ('email', 'ایمیل'),
        ('phone', 'تلفن'),
        ('address', 'آدرس'),
        ('social', 'شبکه اجتماعی'),
    ]

    type = models.CharField(max_length=20, choices=CONTACT_TYPES, verbose_name="نوع")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    value = models.CharField(max_length=200, verbose_name="مقدار")
    icon = models.CharField(max_length=100, verbose_name="آیکون", help_text="کلاس Font Awesome")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "اطلاعات تماس"
        verbose_name_plural = "اطلاعات تماس"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title} - {self.value}"
