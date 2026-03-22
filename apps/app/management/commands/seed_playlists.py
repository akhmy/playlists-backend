import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.app.models import Track, Playlist

User = get_user_model()

PLAYLISTS = [
    ("Morning Vibes", "Лёгкие треки для бодрого начала дня"),
    ("Late Night Drive", "Для ночных поездок по городу"),
    ("Workout Beast Mode", "Качаем железо под правильную музыку"),
    ("Jazz & Coffee", "Джаз под утренний кофе"),
    ("Classic Legends", "Лучшее из классической музыки"),
    ("Hip-Hop Gold", "Золотой фонд хип-хопа"),
    ("Metal Madness", "Для тех кто любит погромче"),
    ("Chill Electronic", "Электронная музыка для расслабления"),
    ("R&B Feelings", "Душевный R&B"),
    ("Rock Anthems", "Рок-гимны всех времён"),
    ("Study Focus", "Концентрация и продуктивность"),
    ("Party Starters", "Открываем вечеринку"),
    ("Sad Hours", "Когда грустно и хочется погрустить"),
    ("90s Throwback", "Лучшее из 90-х"),
    ("Driving Playlist", "В дорогу"),
    ("Sunday Afternoon", "Ленивое воскресенье"),
    ("Underground Gems", "Недооценённые треки"),
    ("Epic Moments", "Музыка для больших моментов"),
    ("Acoustic Sessions", "Тихо и душевно"),
    ("All Time Favourites", "Личный топ на все времена"),
]


class Command(BaseCommand):
    help = 'Seed 20 playlists for user akhmy'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(username='akhmy')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "akhmy" not found. Create it first.'))
            return

        tracks = list(Track.objects.all())
        if not tracks:
            self.stdout.write(self.style.ERROR('No tracks found. Run seed_tracks first.'))
            return

        created = 0
        for name, description in PLAYLISTS:
            if Playlist.objects.filter(name=name, author=user).exists():
                continue
            playlist = Playlist.objects.create(
                name=name,
                description=description,
                author=user,
            )
            count = random.randint(5, 20)
            playlist.tracks.set(random.sample(tracks, min(count, len(tracks))))
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {created}, total: {Playlist.objects.count()}'
        ))
