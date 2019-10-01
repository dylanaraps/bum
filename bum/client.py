"""
Get song info.
"""
import shutil
import mpd
import select
from pkg_resources import iter_entry_points

from . import brainz
from . import util


def get_client_types():
    client_types = {
        'mpd': ClientMPD
    }

    for ep in iter_entry_points("bum_plugin_client"):
        try:
            plugin = ep.load()
            client_types[plugin.option_name] = plugin
        except (ModuleNotFoundError, ImportError) as e:
            print(f"Error loading client plugin {ep}: {e}")

    return client_types


class ClientMPD():
    def __init__(self, port=6600, server="localhost"):
        """Initialize mpd."""
        self._client = mpd.MPDClient()

        try:
            self._client.connect(server, port)

        except ConnectionRefusedError:
            raise RuntimeError("error: Connection refused to mpd/mopidy.")

        self._client.send_idle('player')

    def add_args(argparse):
        pass

    def currentsong(self):
        self._client.noidle()
        result = self._client.currentsong()
        self._client.send_idle('player')
        return result

    def status(self):
        self._client.noidle()
        result = self._client.status()
        self._client.send_idle('player')
        return result

    def update_pending(self, timeout=0):
        result = select.select([self._client], [], [], 0.1)[0]
        return self._client in result

    def get_art(self, cache_dir, size):
        """Get the album art."""
        song = self.currentsong()
        if len(song) < 2:
            print("album: Nothing currently playing.")
            util.bytes_to_file(util.default_album_art, cache_dir / "current.jpg")
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

            if not album_art:
                album_art = util.default_album_art()

            util.bytes_to_file(album_art, cache_dir / file_name)
            util.bytes_to_file(album_art, cache_dir / "current.jpg")

            print(f"album: Swapped art to {song['artist']}, {song['album']}.")
