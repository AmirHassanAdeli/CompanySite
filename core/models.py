from django.db import models


class Service(models.Model):
    icon = models.CharField(max_length=100, default='fas fa-cog')
    title = models.CharField(max_length=200)
    description = models.TextField()

    # کنترل کامل روی ترتیب نمایش محتوا داشته باشید
    """
    نمایش داده ترتیب پروژه ها بر اساس اولویت ها
        پروژه A (order=3)
        پروژه B (order=1)
        پروژه C (order=2)
    """
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='fas fa-cog')
    background_color = models.CharField(
        max_length=200,
        default='linear-gradient(135deg, #00d4ff 0%, #6a5acd 50%, #c0c0c0 100%)'
    )
    technologies = models.TextField(help_text="تکنولوژی‌ها را با کاما(،) جدا کنید")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    telegram = models.CharField(max_length=100)

    def __str__(self):
        return "اطلاعات تماس"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.email}"