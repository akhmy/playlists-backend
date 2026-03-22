from django.core.management.base import BaseCommand
from apps.app.models import Genre

GENRES = [
    "Pop", "Rock", "Hip-Hop", "Electronic", "Jazz",
    "Classical", "R&B", "Metal", "Reggae", "Blues",
    "Country", "Folk", "Soul", "Funk", "Punk",
    "Indie", "Alternative", "Dance", "House", "Techno",
    "Trance", "Drum and Bass", "Dubstep", "Ambient", "Lo-fi",
    "Latin", "Salsa", "Bossa Nova", "Samba", "Afrobeat",
    "Gospel", "Opera", "Soundtrack", "Trap", "Drill",
    "Grunge", "Emo", "Post-Rock", "Psychedelic", "Disco",
    "New Wave", "Synthpop", "Chillout", "Jungle", "Garage",
    "Ska", "Hardrock", "Progressive Rock", "Swing", "K-Pop",
]


class Command(BaseCommand):
    help = 'Seed basic music genres'

    def handle(self, *args, **kwargs):
        created = 0
        for name in GENRES:
            _, is_new = Genre.objects.get_or_create(name=name)
            if is_new:
                created += 1
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {created}, total: {Genre.objects.count()}'
        ))
