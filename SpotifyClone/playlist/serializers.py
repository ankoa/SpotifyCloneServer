from rest_framework import serializers
from .models import Playlist, PlaylistSong, Collection, CollectionSong
from music.models import Song
from user.models import User
class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    songs = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        many=True,
    )
    cover_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Playlist
        fields = '__all__'

class PlaylistSongSerializer(serializers.ModelSerializer):
    playlist = serializers.PrimaryKeyRelatedField(
        queryset=Playlist.objects.all(),
        many=True
    )
    class Meta:
        model = PlaylistSong
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionSong
        fields = '__all__'