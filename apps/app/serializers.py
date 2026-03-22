from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    StringRelatedField,
)
from .models import Track, Playlist, Genre


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class TrackSerializer(ModelSerializer):
    genres = PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Track
        fields = ('id', 'name', 'artists', 'cover', 'genres')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genres'] = GenreSerializer(
            instance.genres.all(), many=True
        ).data
        return representation


class PlaylistListSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    stars = SerializerMethodField()
    already_starred = SerializerMethodField()

    def get_stars(self, obj):
        return obj.stars.count()

    def get_already_starred(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.stars.filter(by=request.user).exists()
        return False

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'cover', 'author', 'stars', 'already_starred')


class PlaylistTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ('id', 'name', 'artists')


class PlaylistUpdateSerializer(ModelSerializer):
    tracks = PrimaryKeyRelatedField(queryset=Track.objects.all(), many=True)

    class Meta:
        model = Playlist
        fields = ('name', 'description', 'cover', 'tracks')


class PlaylistRetrieveSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    tracks = PlaylistTrackSerializer(many=True, read_only=True)
    stars = SerializerMethodField()
    already_starred = SerializerMethodField()

    def get_stars(self, obj):
        return obj.stars.count()

    def get_already_starred(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.stars.filter(by=request.user).exists()
        return False

    class Meta:
        model = Playlist
        fields = (
            'id',
            'name',
            'description',
            'cover',
            'tracks',
            'author',
            'stars',
            'already_starred',
        )
