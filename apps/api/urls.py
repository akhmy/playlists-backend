from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.app.views import TrackViewSet, PlaylistViewSet
from apps.auth.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CookieTokenLogoutView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from apps.users.views import UserRetrieveByUsernameView

router = DefaultRouter()
router.register(prefix='tracks', viewset=TrackViewSet)
router.register(prefix='playlists', viewset=PlaylistViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path(
        'auth/jwt/create/',
        CookieTokenObtainPairView.as_view(),
        name='jwt-create',
    ),
    path(
        'auth/jwt/refresh/',
        CookieTokenRefreshView.as_view(),
        name='jwt-refresh',
    ),
    path(
        'auth/jwt/logout/', CookieTokenLogoutView.as_view(), name='jwt-logout'
    ),
    path('auth/', include('djoser.urls.jwt')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'
    ),
    path(
        'users/<str:username>/',
        UserRetrieveByUsernameView.as_view(),
        name='get-user',
    ),
    path('', include(router.urls)),
]
