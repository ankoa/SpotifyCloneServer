from django.db import models
from user.models import User
# Create your models here.

# Subscription Plan Model
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    features = models.JSONField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# Subscription Model
class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('canceled', 'Canceled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    auto_renew = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['end_date']),
        ]
