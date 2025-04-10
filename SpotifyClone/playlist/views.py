from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Playlist, PlaylistSong, Collection, CollectionSong
from .serializers import PlaylistSerializer, PlaylistSongSerializer, CollectionSerializer, CollectionSongSerializer
from core.views import BaseListCreateView, BaseRetrieveUpdateDestroyView

def custom_response(ec=0, em="Success", dt=None):
    return Response({"EC": ec, "EM": em, "DT": dt}, status=200 if ec == 0 else 400)

# -------------------- PLAYLIST API --------------------
class PlaylistListCreateView(BaseListCreateView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.AllowAny]

class PlaylistDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.AllowAny]

# -------------------- PLAYLIST SONG API --------------------
class PlaylistSongListCreateView(BaseListCreateView):
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer
    permission_classes = [permissions.AllowAny]

class PlaylistSongDetailView(BaseRetrieveUpdateDestroyView):
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer
    permission_classes = [permissions.AllowAny]

# -------------------- COLLECTION API --------------------
class CollectionListCreateView(BaseListCreateView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.AllowAny]

class CollectionDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.AllowAny]

# -------------------- COLLECTION SONG API --------------------
class CollectionSongListCreateView(BaseListCreateView):
    queryset = CollectionSong.objects.all()
    serializer_class = CollectionSongSerializer
    permission_classes = [permissions.AllowAny]

class CollectionSongDetailView(BaseRetrieveUpdateDestroyView):
    queryset = CollectionSong.objects.all()
    serializer_class = CollectionSongSerializer
    permission_classes = [permissions.AllowAny]
