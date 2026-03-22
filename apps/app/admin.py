from django.contrib import admin
from .models import Genre, Track, Star, Playlist

# Register your models here.
admin.site.register(Genre)
admin.site.register(Track)
admin.site.register(Star)
admin.site.register(Playlist)
