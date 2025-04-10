from django.db import models
from user.models import User
from music.models import Song
from music.models import Album
# Create your models here.
# Favorite Album Model
class FavoriteAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_albums')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='favorited_by')
    favorited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'album')
        indexes = [
            models.Index(fields=['user', 'album']),
        ]

# Favorite Song Model
class FavoriteSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorited_by')
    favorited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'song')
        indexes = [
            models.Index(fields=['user', 'song']),
        ]
