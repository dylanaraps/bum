"""
Get song info.
"""
import shutil
import sys

from . import brainz
from . import util


def get_player():
    """Detect music player."""
    players = ["mpd", "mopidy", "cmus"]
    player = [player for player in players if util.get_pid(player)]
    return player[0]


def get_song(player, port):
    """Get current song."""
    if player in ["mpd", "mopidy"]:
        from .players import musicpd
        client = musicpd.init(port)
        return musicpd.get_song(client)

    elif player == "cmus":
        from .players import cmus
        client = cmus.init(port)
        return cmus.get_song(client)

    else:
        print("error: No music player found.")
        sys.exit(1)


def get_art(cache_dir, size, player, port):
    """Get the album art."""
    song = get_song(player, port)

    if len(song) < 2:
        print("album: Nothing currently playing.")
        return

    if "album" not in song or "artist" not in song:
        print("album: Tags are missing, skipping track.")
        return

    file_name = f"{song['artist']}_{song['album']}_{size}.jpg".replace("/", "")
    file_name = cache_dir / file_name

    if file_name.is_file():
        shutil.copy(file_name, cache_dir / "current.jpg")
        print("album: Found cached art.")

    else:
        print("album: Downloading album art...")

        brainz.init()
        album_art = brainz.get_cover(song, size)

        if album_art:
            util.bytes_to_file(album_art, cache_dir / file_name)
            util.bytes_to_file(album_art, cache_dir / "current.jpg")

            print(f"album: Swapped art to {song['artist']}, {song['album']}.")
