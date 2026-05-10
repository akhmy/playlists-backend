import random
from locust import HttpUser, task, between


class AnonymousUser(HttpUser):
    weight = 3
    wait_time = between(1, 3)

    def on_start(self):
        resp = self.client.get("/api/v1/playlists/").json()
        self._playlist_ids = [p["id"] for p in resp.get("results", [])] or [1]

        resp = self.client.get("/api/v1/tracks/").json()
        self._track_ids = [t["id"] for t in resp.get("results", resp if isinstance(resp, list) else [])] or [1]

    @task(4)
    def list_playlists(self):
        self.client.get("/api/v1/playlists/")

    @task(3)
    def trending_playlists(self):
        self.client.get("/api/v1/playlists/trending/")

    @task(2)
    def get_playlist(self):
        self.client.get(f"/api/v1/playlists/{random.choice(self._playlist_ids)}/")

    @task(2)
    def list_tracks(self):
        self.client.get("/api/v1/tracks/")

    @task(1)
    def search_tracks(self):
        query = random.choice(["rock", "pop", "jazz", "metal", "indie"])
        self.client.get(f"/api/v1/tracks/?search={query}")

    @task(1)
    def get_track(self):
        self.client.get(f"/api/v1/tracks/{random.choice(self._track_ids)}/")


class AuthenticatedUser(HttpUser):
    weight = 1
    wait_time = between(1, 5)

    def on_start(self):
        uid = random.randint(1, 100000)
        self._username = f"loaduser_{uid}"
        self._password = "loadpass123"

        self.client.post(
            "/api/v1/auth/users/",
            json={"username": self._username, "password": self._password, "email": f"{self._username}@test.com"},
        )

        resp = self.client.post(
            "/api/v1/auth/jwt/create/",
            json={"username": self._username, "password": self._password},
        ).json()
        token = resp.get("access", "")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        resp = self.client.get("/api/v1/playlists/").json()
        self._playlist_ids = [p["id"] for p in resp.get("results", [])] or [1]

    @task(3)
    def list_playlists(self):
        self.client.get("/api/v1/playlists/")

    @task(2)
    def get_playlist(self):
        self.client.get(f"/api/v1/playlists/{random.choice(self._playlist_ids)}/")

    @task(2)
    def upvote_playlist(self):
        self.client.patch(f"/api/v1/playlists/{random.choice(self._playlist_ids)}/upvote/")

    @task(1)
    def create_playlist(self):
        self.client.post(
            "/api/v1/playlists/",
            json={"name": f"Load playlist {random.randint(1, 9999)}", "description": "", "tracks": []},
        )
