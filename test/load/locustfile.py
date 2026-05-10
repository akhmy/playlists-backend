import random
from locust import HttpUser, task, between


class AnonymousUser(HttpUser):
    weight = 3
    wait_time = between(1, 3)

    def on_start(self):
        resp = self.client.get("/api/v1/playlists/").json()
        self._playlist_ids = [p["id"] for p in resp.get("results", [])]

        resp = self.client.get("/api/v1/tracks/").json()
        results = resp if isinstance(resp, list) else resp.get("results", [])
        self._track_ids = [t["id"] for t in results]

    @task(4)
    def list_playlists(self):
        self.client.get("/api/v1/playlists/")

    @task(3)
    def trending_playlists(self):
        self.client.get("/api/v1/playlists/trending/")

    @task(2)
    def get_playlist(self):
        if self._playlist_ids:
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
        if self._track_ids:
            self.client.get(f"/api/v1/tracks/{random.choice(self._track_ids)}/")


class AuthenticatedUser(HttpUser):
    weight = 1
    wait_time = between(1, 5)

    def on_start(self):
        uid = random.randint(1, 1_000_000)
        self._username = f"loaduser_{uid}"
        self._password = f"Ld#{uid}!xQ9"
        self._authenticated = False
        self._playlist_ids = []

        reg = self.client.post(
            "/api/v1/auth/users/",
            json={"username": self._username, "password": self._password, "re_password": self._password, "email": f"{self._username}@test.com"},
        )
        if not reg.ok:
            return

        resp = self.client.post(
            "/api/v1/auth/jwt/create/",
            json={"username": self._username, "password": self._password},
        ).json()
        token = resp.get("access")
        if not token:
            return

        self.client.headers.update({"Authorization": f"Bearer {token}"})
        self._authenticated = True

        resp = self.client.get("/api/v1/playlists/").json()
        self._playlist_ids = [p["id"] for p in resp.get("results", [])]

    @task(3)
    def list_playlists(self):
        self.client.get("/api/v1/playlists/")

    @task(2)
    def get_playlist(self):
        if self._playlist_ids:
            self.client.get(f"/api/v1/playlists/{random.choice(self._playlist_ids)}/")

    @task(2)
    def upvote_playlist(self):
        if self._authenticated and self._playlist_ids:
            self.client.patch(f"/api/v1/playlists/{random.choice(self._playlist_ids)}/upvote/")

    @task(1)
    def create_playlist(self):
        if self._authenticated:
            self.client.post(
                "/api/v1/playlists/",
                json={"name": f"Load playlist {random.randint(1, 9999)}", "description": "", "tracks": []},
            )
