from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework.serializers import SerializerMethodField


class UserSerializer(BaseUserSerializer):
    stars = SerializerMethodField()

    def get_stars(self, obj):
        from django.db.models import Count

        return obj.playlists.aggregate(total=Count('stars'))['total']

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + (
            'avatar',
            'bio',
            'is_staff',
            'stars',
        )


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('username', 'password', 're_password')
