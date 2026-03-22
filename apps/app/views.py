from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Track, Playlist, Star
from .serializers import (
    TrackSerializer,
    PlaylistListSerializer,
    PlaylistRetrieveSerializer,
    PlaylistUpdateSerializer,
)
from django.utils import timezone
from django.db import models
from .pagination import StandardPagination


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def get_queryset(self):
        qs = Track.objects.all()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    def perform_create(self, serializer):
        serializer.save()


class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return PlaylistListSerializer
        if self.action == 'retrieve':
            return PlaylistRetrieveSerializer
        if self.action in ('update', 'partial_update', 'create'):
            return PlaylistUpdateSerializer
        return PlaylistListSerializer

    @property
    def pagination_class(self):
        if self.action == 'list':
            return StandardPagination
        return None

    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request):
        week_ago = timezone.now() - timezone.timedelta(days=7)
        playlists = Playlist.objects.annotate(
            week_stars=models.Count(
                'stars', filter=models.Q(stars__datetime__gte=week_ago)
            )
        ).order_by('-week_stars', 'name')[:16]
        serializer = PlaylistListSerializer(
            playlists, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='upvote')
    def upvote(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        playlist = self.get_object()
        star_qs = playlist.stars.filter(by=request.user)

        if star_qs.exists():
            star_qs.delete()
        else:
            Star.objects.create(
                by=request.user, playlist=playlist, datetime=timezone.now()
            )

        return Response(
            {
                'stars': playlist.stars.count(),
                'already_starred': playlist.stars.filter(
                    by=request.user
                ).exists(),
            },
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
