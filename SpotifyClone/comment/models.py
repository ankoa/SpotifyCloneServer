from django.db import models
from user.models import User
from music.models import Song
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        indexes = [
            models.Index(fields=['song']),
            models.Index(fields=['created_at']),
        ]
# Rating Model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'song')
        indexes = [
            models.Index(fields=['song']),
            models.Index(fields=['rating']),
        ]
