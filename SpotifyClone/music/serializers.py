from rest_framework import serializers
from .models import Genre, Artist, ArtistFollow, Album, Song, SongRecommendation, ListeningHistory

# Genre Serializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

# Artist Serializer
class ArtistSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True
    )
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Artist
        fields = '__all__'

# Artist Follow Serializer
class ArtistFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistFollow
        fields = '__all__'

# Album Serializer
class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all()
    )
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True
    )
    cover_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Album
        fields = '__all__'

# Song Serializer
class SongSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())  # Cho phép nhập ID của Artist
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)  # Nhận danh sách ID của Genre
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Song
        fields = '__all__'

    def validate_file(self, value):
        """ Kiểm tra nếu là video/audio thì cho phép """
        mime = magic.from_buffer(value.read(1024), mime=True)
        value.seek(0)
        if not mime.startswith(('audio/', 'video/')):
            raise serializers.ValidationError("Chỉ chấp nhận file âm thanh hoặc video!")
        return value

# Song Recommendation Serializer
class SongRecommendationSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = SongRecommendation
        fields = '__all__'

# Listening History Serializer
class ListeningHistorySerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = ListeningHistory
        fields = '__all__'
