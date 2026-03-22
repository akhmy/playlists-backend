from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=256)
    artists = models.CharField(max_length=256)
    cover = models.ImageField(
        upload_to='covers/tracks/', blank=True, null=True
    )
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return f'{self.artists} — {self.name}'


class Playlist(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default="")
    cover = models.ImageField(
        upload_to='covers/playlists/', blank=True, null=True
    )

    tracks = models.ManyToManyField(Track)
    author = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='playlists'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} — {self.name}'


class Star(models.Model):
    by = models.ForeignKey(
        'users.User', related_name='stars', on_delete=models.CASCADE
    )
    playlist = models.ForeignKey(
        Playlist, related_name='stars', on_delete=models.CASCADE
    )
    datetime = models.DateTimeField()

    def __str__(self):
        return f"By {self.by} to '{self.playlist}' at {self.datetime}"
