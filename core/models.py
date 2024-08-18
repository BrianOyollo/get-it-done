from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.


class ReportStatus(models.Model):
    status = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Report Statuses"
        ordering = ('status',)

    def __str__(self):
        return self.status[:50]


class Category(models.Model):
    category = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=250, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Report Categories"
        ordering = ('category',)

    def __str__(self):
        return self.category


class Subcategory(models.Model):
    subcategory = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=250, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Report Subcategories"
        ordering = ('subcategory',)

    def __str__(self):
        return self.subcategory
    

class Report(models.Model):
    description = models.TextField(max_length=500, blank=False, null=False)
    location = models.CharField(max_length=150, null=False, blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=False, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, blank=False, null=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    status = models.ForeignKey(ReportStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    responsible_party = models.CharField(max_length=50, null=True, blank=True)
    responsible_party_contact = models.CharField(max_length=100, null=True, blank=True)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    reporter_contact = models.CharField(max_length=100, null=True, blank=True)
    reporter_confirm_fix_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Reports"
        ordering = ('-created_at',)

    def __str__(self):
        return self.description[:50]
    

class ModeratorApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=25, null=False, blank=False, default='John')
    last_name = models.CharField(max_length=25, null=False, blank=False, default='Doe')
    location = models.CharField(max_length=150, blank=False, null=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Moderator Applications"
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.username

class Moderator(models.Model):
    location = models.CharField(max_length=100, blank=False, null=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, related_name='moderator', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moderator')

    class Meta:
        verbose_name_plural = "Moderators"

    def __str__(self):
        return self.user.username

class ModeratorAction(models.Model):
    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE, related_name='actions')
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True,  related_name='actions')
    status = models.ForeignKey(ReportStatus, on_delete=models.SET_NULL, null=True, related_name='actions')
    action_description = models.TextField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Moderator Actions"
        ordering = ('-created_at',)

    def __str__(self):
        return self.moderator


class ReportFile(models.Model):
    file = models.FileField(upload_to='report_files/', blank=False, null=False)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Report Files"
        ordering = ('report',)

    def __str__(self):
        return self.file.name
    



















