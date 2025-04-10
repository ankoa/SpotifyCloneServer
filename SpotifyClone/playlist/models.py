from django.db import models
from user.models import User
from music.models import Song
from music.models import Genre
from cloudinary.models import CloudinaryField

# Create your models here.
# Playlist Model
class Playlist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ManyToManyField(Song, through='PlaylistSong', related_name='playlists')
    cover_image = CloudinaryField('playlist_covers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_public']),
            models.Index(fields=['slug']),
        ]

# PlaylistSong Model (for ordered songs in playlist)
class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('playlist', 'song')
        ordering = ['position']
        indexes = [
            models.Index(fields=['playlist', 'position']),
        ]
# Song Collection Model (Featured playlists, trending, etc.)
class Collection(models.Model):
    COLLECTION_TYPES = (
        ('featured', 'Featured'),
        ('trending', 'Trending'),
        ('new_releases', 'New Releases'),
        ('genre_based', 'Genre Based'),
        ('mood_based', 'Mood Based'),
        ('seasonal', 'Seasonal'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    collection_type = models.CharField(max_length=20, choices=COLLECTION_TYPES)
    cover_image = CloudinaryField('collection_covers', null=True, blank=True)
    songs = models.ManyToManyField(Song, through='CollectionSong', related_name='collections')
    genres = models.ManyToManyField(Genre, related_name='collections', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        indexes = [
            models.Index(fields=['collection_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['slug']),
        ]

# Collection Song Model (for ordered songs in collections)
class CollectionSong(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('collection', 'song')
        ordering = ['position']