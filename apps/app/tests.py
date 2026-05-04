from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Genre, Track, Playlist, Star
from django.utils import timezone

User = get_user_model()


class TrackModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Rock')
        self.track = Track.objects.create(name='Bohemian Rhapsody', artists='Queen')
        self.track.genres.add(self.genre)

    def test_track_str(self):
        self.assertEqual(str(self.track), 'Queen — Bohemian Rhapsody')

    def test_track_genre(self):
        self.assertIn(self.genre, self.track.genres.all())


class PlaylistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='pass1234')
        self.playlist = Playlist.objects.create(name='My Mix', author=self.user)

    def test_playlist_str(self):
        self.assertIn('My Mix', str(self.playlist))

    def test_playlist_author(self):
        self.assertEqual(self.playlist.author, self.user)

    def test_playlist_default_description(self):
        self.assertEqual(self.playlist.description, '')


class StarModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='fan', password='pass1234')
        self.author = User.objects.create_user(username='creator', password='pass1234')
        self.playlist = Playlist.objects.create(name='Hits', author=self.author)

    def test_star_created(self):
        star = Star.objects.create(by=self.user, playlist=self.playlist, datetime=timezone.now())
        self.assertEqual(self.playlist.stars.count(), 1)
        self.assertEqual(star.by, self.user)

    def test_star_deleted_with_user(self):
        Star.objects.create(by=self.user, playlist=self.playlist, datetime=timezone.now())
        self.user.delete()
        self.assertEqual(self.playlist.stars.count(), 0)


class TrackAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.track = Track.objects.create(name='Stairway', artists='Led Zeppelin')

    def test_list_tracks(self):
        response = self.client.get('/api/v1/tracks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_tracks(self):
        Track.objects.create(name='Highway to Hell', artists='AC/DC')
        response = self.client.get('/api/v1/tracks/?search=stair')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Stairway')


class PlaylistAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.playlist = Playlist.objects.create(name='Chill', author=self.user)

    def test_list_playlists(self):
        response = self.client.get('/api/v1/playlists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trending_endpoint(self):
        response = self.client.get('/api/v1/playlists/trending/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upvote_requires_auth(self):
        response = self.client.patch(f'/api/v1/playlists/{self.playlist.pk}/upvote/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upvote_adds_star(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/v1/playlists/{self.playlist.pk}/upvote/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stars'], 1)
        self.assertTrue(response.data['already_starred'])

    def test_upvote_twice_removes_star(self):
        self.client.force_authenticate(user=self.user)
        self.client.patch(f'/api/v1/playlists/{self.playlist.pk}/upvote/')
        response = self.client.patch(f'/api/v1/playlists/{self.playlist.pk}/upvote/')
        self.assertEqual(response.data['stars'], 0)
        self.assertFalse(response.data['already_starred'])
