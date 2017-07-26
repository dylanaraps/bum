"""
Get song info.
"""
import shutil
import subprocess

from . import brainz
from . import util


def get():
    """Get the current playing song."""
    song = subprocess.getoutput("mpc current -f \
                                 '%albumartist%💩%title%💩%album%'")

    if song:
        return song.split("💩")


def get_art(cache_dir):
    """Get the album art."""
    song_data = get()

    if not song_data:
        print("Nothing currently playing.")
        return

    file_name = f"{song_data[0]}_{song_data[2]}.jpg".replace("/", "")
    file_name = cache_dir / file_name

    if file_name.is_file():
        shutil.copy(file_name, cache_dir / "current.jpg")
        print("album: Found cached art.")

    else:
        print("album: Downloading album art...")

        brainz.init()
        album_art = brainz.get_cover(song_data)

        if album_art:
            util.bytes_to_file(album_art, cache_dir / file_name)
            util.bytes_to_file(album_art, cache_dir / "current.jpg")

            print(f"album: Swapped art to {', '.join(song_data)}.")
