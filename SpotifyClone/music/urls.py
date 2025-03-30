from django.urls import path
from .views import (
    GenreListCreateView, GenreDetailView,
    ArtistListCreateView, ArtistDetailView, FollowArtistView,
    AlbumListCreateView, AlbumDetailView,
    SongListCreateView, SongDetailView, IncreasePlayCountView,
    SongRecommendationListView,
    ListeningHistoryListCreateView, ListeningHistoryDetailView
)

urlpatterns = [
    # Genre URLs
    path('genres/', GenreListCreateView.as_view(), name='genre-list-create'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),

    # Artist URLs
    path('artists/', ArtistListCreateView.as_view(), name='artist-list-create'),
    path('artists/<int:pk>/', ArtistDetailView.as_view(), name='artist-detail'),
    path('artists/<int:artist_id>/follow/', FollowArtistView.as_view(), name='artist-follow'),

    # Album URLs
    path('albums/', AlbumListCreateView.as_view(), name='album-list-create'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),

    # Song URLs
    path('songs/', SongListCreateView.as_view(), name='song-list-create'),
    path('songs/<int:pk>/', SongDetailView.as_view(), name='song-detail'),
    path('songs/<int:song_id>/play/', IncreasePlayCountView.as_view(), name='increase-play-count'),

    # Song Recommendation URLs
    path('recommendations/', SongRecommendationListView.as_view(), name='song-recommendations'),

    # Listening History URLs
    path('listening-history/', ListeningHistoryListCreateView.as_view(), name='listening-history-list-create'),
    path('listening-history/<int:pk>/', ListeningHistoryDetailView.as_view(), name='listening-history-detail'),
]
