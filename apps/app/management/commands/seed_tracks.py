from django.core.management.base import BaseCommand
from apps.app.models import Genre, Track

TRACKS = [
    ("Blinding Lights", "The Weeknd", ["Pop", "Electronic"]),
    ("Bohemian Rhapsody", "Queen", ["Rock"]),
    ("HUMBLE.", "Kendrick Lamar", ["Hip-Hop"]),
    ("Strobe", "deadmau5", ["Electronic"]),
    ("So What", "Miles Davis", ["Jazz"]),
    ("Moonlight Sonata", "Beethoven", ["Classical"]),
    ("No One", "Alicia Keys", ["R&B", "Pop"]),
    ("Master of Puppets", "Metallica", ["Metal", "Rock"]),
    ("Shape of You", "Ed Sheeran", ["Pop"]),
    ("God's Plan", "Drake", ["Hip-Hop", "R&B"]),
    ("Levels", "Avicii", ["Electronic", "Pop"]),
    ("Take Five", "Dave Brubeck", ["Jazz"]),
    ("Symphony No. 5", "Beethoven", ["Classical"]),
    ("Crazy in Love", "Beyoncé", ["R&B", "Pop"]),
    ("Enter Sandman", "Metallica", ["Metal"]),
    ("Rolling in the Deep", "Adele", ["Pop", "Rock"]),
    ("SICKO MODE", "Travis Scott", ["Hip-Hop"]),
    ("One More Time", "Daft Punk", ["Electronic"]),
    ("Autumn Leaves", "Bill Evans", ["Jazz"]),
    ("Clair de Lune", "Debussy", ["Classical"]),
    ("Kiss", "Prince", ["R&B", "Pop"]),
    ("Black Dog", "Led Zeppelin", ["Rock"]),
    ("Lose Yourself", "Eminem", ["Hip-Hop"]),
    ("Around the World", "Daft Punk", ["Electronic"]),
    ("All Blues", "Miles Davis", ["Jazz"]),
    ("The Four Seasons", "Vivaldi", ["Classical"]),
    ("I Will Always Love You", "Whitney Houston", ["R&B", "Pop"]),
    ("Paranoid", "Black Sabbath", ["Metal", "Rock"]),
    ("As It Was", "Harry Styles", ["Pop"]),
    ("MONTERO", "Lil Nas X", ["Hip-Hop", "Pop"]),
    ("Sandstorm", "Darude", ["Electronic"]),
    ("Blue in Green", "Miles Davis", ["Jazz"]),
    ("Für Elise", "Beethoven", ["Classical"]),
    ("I'd Rather Go Blind", "Etta James", ["R&B"]),
    ("Whole Lotta Love", "Led Zeppelin", ["Rock"]),
    ("Alright", "Kendrick Lamar", ["Hip-Hop"]),
    ("Smells Like Teen Spirit", "Nirvana", ["Rock"]),
    ("Frequency", "Zedd", ["Electronic"]),
    ("My Favorite Things", "John Coltrane", ["Jazz"]),
    ("Requiem in D Minor", "Mozart", ["Classical"]),
    ("Let's Stay Together", "Al Green", ["R&B"]),
    ("Iron Man", "Black Sabbath", ["Metal"]),
    ("Flowers", "Miley Cyrus", ["Pop"]),
    ("Scary Monsters and Nice Sprites", "Skrillex", ["Electronic"]),
    ("Summertime", "John Coltrane", ["Jazz"]),
    ("Gymnopédie No.1", "Satie", ["Classical"]),
    ("Superstition", "Stevie Wonder", ["R&B"]),
    ("War Pigs", "Black Sabbath", ["Metal", "Rock"]),
    ("Anti-Hero", "Taylor Swift", ["Pop"]),
    ("GOD", "Kendrick Lamar", ["Hip-Hop"]),
    ("Blue (Da Ba Dee)", "Eiffel 65", ["Electronic", "Pop"]),
    ("Round Midnight", "Thelonious Monk", ["Jazz"]),
    ("Bolero", "Ravel", ["Classical"]),
    ("Killing Me Softly", "Roberta Flack", ["R&B"]),
    ("Battery", "Metallica", ["Metal"]),
    ("Bad Guy", "Billie Eilish", ["Pop"]),
    ("Power", "Kanye West", ["Hip-Hop"]),
    ("Fly Me to the Moon", "Frank Sinatra", ["Jazz"]),
    ("Swan Lake", "Tchaikovsky", ["Classical"]),
    ("Respect", "Aretha Franklin", ["R&B"]),
    ("Highway to Hell", "AC/DC", ["Rock"]),
    ("New York State of Mind", "Jay-Z", ["Hip-Hop"]),
    ("Numb", "Linkin Park", ["Rock"]),
    ("Music Sounds Better with You", "Stardust", ["Electronic"]),
    ("Giant Steps", "John Coltrane", ["Jazz"]),
    ("Nocturne Op.9 No.2", "Chopin", ["Classical"]),
    ("Sexual Healing", "Marvin Gaye", ["R&B"]),
    ("The Number of the Beast", "Iron Maiden", ["Metal"]),
    ("Watermelon Sugar", "Harry Styles", ["Pop"]),
    ("Ultralight Beam", "Kanye West", ["Hip-Hop"]),
    ("Titanium", "David Guetta ft. Sia", ["Electronic", "Pop"]),
    ("Georgia on My Mind", "Ray Charles", ["Jazz", "R&B"]),
    ("Ain't No Sunshine", "Bill Withers", ["R&B"]),
    ("Raining Blood", "Slayer", ["Metal"]),
    ("Levitating", "Dua Lipa", ["Pop"]),
    ("Stronger", "Kanye West", ["Hip-Hop", "Electronic"]),
    ("Mr. Brightside", "The Killers", ["Rock"]),
    ("Midnight City", "M83", ["Electronic"]),
    ("Autumn in New York", "Ella Fitzgerald", ["Jazz"]),
    ("I Put a Spell on You", "Nina Simone", ["R&B", "Jazz"]),
    ("Fade to Black", "Metallica", ["Metal"]),
    ("Cruel Summer", "Taylor Swift", ["Pop"]),
    ("Started from the Bottom", "Drake", ["Hip-Hop"]),
    ("Believer", "Imagine Dragons", ["Rock", "Electronic"]),
    ("What a Wonderful World", "Louis Armstrong", ["Jazz"]),
    ("Ode to Joy", "Beethoven", ["Classical"]),
    ("I Feel Good", "James Brown", ["R&B"]),
    ("Holy Wars", "Megadeth", ["Metal"]),
    ("Landslide", "Fleetwood Mac", ["Rock"]),
    ("Through the Wire", "Kanye West", ["Hip-Hop"]),
    ("Pump Up the Jam", "Technotronic", ["Electronic", "Pop"]),
    ("La Grange", "ZZ Top", ["Rock", "Blues"]),
    ("Juicy", "The Notorious B.I.G.", ["Hip-Hop"]),
    ("Oxygène", "Jean-Michel Jarre", ["Electronic"]),
    ("Round About Midnight", "Miles Davis", ["Jazz"]),
    ("Pictures at an Exhibition", "Mussorgsky", ["Classical"]),
    ("Halo", "Beyoncé", ["R&B", "Pop"]),
    ("South of Heaven", "Slayer", ["Metal"]),
    ("Someone Like You", "Adele", ["Pop"]),
    ("99 Problems", "Jay-Z", ["Hip-Hop", "Rock"]),
]


class Command(BaseCommand):
    help = 'Seed 100 tracks'

    def handle(self, *args, **kwargs):
        genres_cache = {g.name: g for g in Genre.objects.all()}
        created = 0

        for name, artists, genre_names in TRACKS:
            if Track.objects.filter(name=name, artists=artists).exists():
                continue
            track = Track.objects.create(name=name, artists=artists)
            track.genres.set([
                genres_cache[g] for g in genre_names if g in genres_cache
            ])
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {created}, total: {Track.objects.count()}'
        ))
