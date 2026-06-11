from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User


class Provider(models.Model):
    ROLE = "provider"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, default=ROLE, editable=False)
    trial_start = models.DateTimeField(default=timezone.now)
    trial_end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.trial_end:
            self.trial_end = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def is_trial_expired(self):
        return timezone.now() > self.trial_end

    def __str__(self):
        return self.full_name


class ServiceProfile(models.Model):
    SERVICE_CHOICES = [
        ("none", "None"),
        ("electrician", "Electrician"),
        ("plumber", "Plumber"),
        ("carpenter", "Carpenter"),
        ("cleaning", "Cleaning"),
        ("painter", "Painter"),
        ("mechanic", "Mechanic"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    business_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    available_days = models.CharField(max_length=255)
    available_time = models.CharField(max_length=255)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.CharField(max_length=50,choices=SERVICE_CHOICES,default="none")

    latitude = models.FloatField(max_length=255, blank=True, null=True)
    longitude = models.FloatField(max_length=255, blank=True, null=True)

      # Rating & reviews (updated manually or via signal/aggregation)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)

    # Optional social media URLs
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)

    is_shop = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class ServiceItem(models.Model):
    profile = models.ForeignKey(ServiceProfile, on_delete=models.CASCADE, related_name="services")
    service_name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service_name
    

class ProviderPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='provider/images/', blank=True, null=True)
    video = models.FileField(upload_to='provider/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title