from django.db import models
from user.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.core.validators import FileExtensionValidator
import os
import mimetypes
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
def custom_validate_video(file):
    """ Kiểm tra định dạng video và kích thước file """

    if not file:
        raise ValidationError("Không có file được tải lên.")

    # Kiểm tra phần mở rộng hợp lệ
    valid_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv']
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError("Không hỗ trợ định dạng video này.")

    # Lấy MIME type bằng mimetypes
    mime_type, _ = mimetypes.guess_type(file.name)

    if not mime_type or not mime_type.startswith("video/"):
        raise ValidationError("File tải lên không phải là video hợp lệ.")

    # Kiểm tra kích thước file (giới hạn 500MB)
    if file.size > 500 * 1024 * 1024:
        raise ValidationError("File quá lớn, vui lòng tải lên file nhỏ hơn 500MB.")

    return file
# Create your models here.
# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Artist Model
class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    image = CloudinaryField('artist_images', null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='artists')
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

# Artist Follow Model
class ArtistFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist_follows')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'artist')
        indexes = [
            models.Index(fields=['user', 'artist']),
        ]

# Album Model
class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    genres = models.ManyToManyField(Genre, related_name='albums')
    release_date = models.DateField()
    cover_image = CloudinaryField('album_covers', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    class Meta:
        unique_together = ('title', 'artist')
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_date']),
            models.Index(fields=['slug']),
        ]

#------------------------------------------------------------------------------------------------------------------------------------------------------
video_storage = MediaCloudinaryStorage(resource_type='video')
audio_storage = MediaCloudinaryStorage(resource_type='raw')
def custom_validate_video(file):
    import os
    from django.core.exceptions import ValidationError
    
    valid_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv']
    
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Không hỗ trợ định dạng video này.')
    
    if file.size > 500 * 1024 * 1024:  # 500MB
        raise ValidationError('File quá lớn, vui lòng tải lên file nhỏ hơn 500MB.')
    
    return file

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    featuring_artists = models.ManyToManyField(Artist, related_name='featured_in', blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True, related_name='songs')
    genres = models.ManyToManyField(Genre, related_name='songs')
    composers = models.ManyToManyField(Artist, related_name='composed_songs')

    audio_file = models.FileField(
        storage=audio_storage,  # Sử dụng storage với resource_type='raw'
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'flac'])]
    )

    video_file = models.FileField(
        storage=video_storage,  # Sử dụng storage với resource_type='video'
        validators=[custom_validate_video], 
        null=True, blank=True
    )

    duration = models.DurationField()
    lyrics = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_downloadable = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    play_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.release_date and self.album:
            self.release_date = self.album.release_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_date']),
            models.Index(fields=['play_count']),
            models.Index(fields=['is_premium']),
            models.Index(fields=['slug']),
        ]

# Song Recommendation Model
class SongRecommendation(models.Model):
    RECOMMENDATION_TYPES = (
        ('listening_history', 'Based on Listening History'),
        ('similar_users', 'Based on Similar Users'),
        ('genre_preference', 'Based on Genre Preference'),
        ('trending', 'Trending Songs'),
        ('new_release', 'New Releases'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='recommended_to')
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPES)
    score = models.FloatField()  # Relevance score for recommendation
    reason = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'song', 'recommendation_type')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['score']),
            models.Index(fields=['is_seen']),
            models.Index(fields=['created_at']),
        ]
# Listening History Model
class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='listened_by')
    listened_at = models.DateTimeField(auto_now_add=True)
    listened_duration = models.DurationField(null=True, blank=True)  # How long user listened
    play_position = models.DurationField(null=True, blank=True)  # Where user left off
    completed = models.BooleanField(default=False)  # If user listened to the entire song
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['listened_at']),
            models.Index(fields=['completed']),
        ]
