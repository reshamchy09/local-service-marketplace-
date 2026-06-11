from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User

class Dealer(models.Model):
    ROLE = "dealer"
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    business_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
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