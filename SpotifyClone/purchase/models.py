from django.db import models
from user.models import User
from music.models import Song

# Create your models here.
# Purchase Model
class Purchase(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        unique_together = ('user', 'song')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['purchase_date']),
            models.Index(fields=['status']),
        ]
