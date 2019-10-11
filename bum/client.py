"""
Get song info.
"""
import shutil
import select
from pkg_resources import iter_entry_points

import mpd

from . import brainz
from . import util


def get_client_types():
    """Enumerate the bum_plugin_client entry point and return installed client types."""
    client_types = {
        'mpd': ClientMPD
    }

    for entry_point in iter_entry_points("bum_plugin_client"):
        try:
            plugin = entry_point.load()
            client_types[plugin.option_name] = plugin
        except (ModuleNotFoundError, ImportError) as err:
            print(f"Error loading client plugin {entry_point}: {err}")

    return client_types


class ClientMPD():
    """Client for MPD and MPD-like (such as Mopidy) music back-ends."""
    def __init__(self, port=6600, server="localhost"):
        """Initialize mpd."""
        self._client = mpd.MPDClient()

        try:
            self._client.connect(server, port)

        except ConnectionRefusedError:
            raise RuntimeError("error: Connection refused to mpd/mopidy.")

        self._client.send_idle('player')

    def add_args(argparse):  # pylint: disable=no-self-argument
        """Expand argparse instance with client-specific args."""

    def currentsong(self):
        """Return current song details."""
        self._client.noidle()
        result = self._client.currentsong()  # pylint: disable=no-member
        self._client.send_idle('player')
        return result

    def status(self):
        """Return current status details."""
        self._client.noidle()
        result = self._client.status()  # pylint: disable=no-member
        self._client.send_idle('player')
        return result

    def update_pending(self, timeout=0.1):
        """Determine if anything has changed on the server."""
        result = select.select([self._client], [], [], timeout)[0]
        return self._client in result

    def get_art(self, cache_dir, size):
        """Get the album art."""
        song = self.currentsong()
        if len(song) < 2:
            print("album: Nothing currently playing.")
            util.bytes_to_file(util.default_album_art, cache_dir / "current.jpg")
            return

        artist = song.get('artist')
        title = song.get('title')
        album = song.get('album', title)
        file_name = f"{artist}_{album}_{size}.jpg".replace("/", "")
        file_name = cache_dir / file_name

        if file_name.is_file():
            shutil.copy(file_name, cache_dir / "current.jpg")
            print("album: Found cached art.")

        else:
            print("album: Downloading album art...")

            brainz.init()
            album_art = brainz.get_cover(song, size)

            if not album_art:
                album_art = util.default_album_art()

            util.bytes_to_file(album_art, cache_dir / file_name)
            util.bytes_to_file(album_art, cache_dir / "current.jpg")

            print(f"album: Swapped art to {artist}, {title}.")
