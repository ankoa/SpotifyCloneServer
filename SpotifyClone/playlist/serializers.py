from rest_framework import serializers
from .models import Playlist, PlaylistSong, Collection, CollectionSong
from music.models import Song

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'

class PlaylistSongSerializer(serializers.ModelSerializer):
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