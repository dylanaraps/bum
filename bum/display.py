"""
Display Output Classes.
"""
from pkg_resources import iter_entry_points


def get_display_types():
    """Enumerate the bum_plugin_display entry point and return installed display types."""
    display_types = {
        'dummy': DisplayDummy,
        'mpv': DisplayMPV,
    }

    for entry_point in iter_entry_points("bum_plugin_display"):
        try:
            plugin = entry_point.load()
            display_types[plugin.option_name] = plugin
        except (ModuleNotFoundError, ImportError) as err:
            print(f"Error loading display plugin {entry_point}: {err}")

    return display_types


class Display():
    """Base class to represent a bum display output."""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, args=None):
        """Initialise a new display."""
        self._size = args.size
        self._title = ''
        self._shuffle = False
        self._repeat = False
        self._state = ''
        self._volume = 0
        self._progress = 0
        self._elapsed = 0

        self._title = ''
        self._album = ''
        self._artist = ''

    def update_album_art(self, input_file):
        """Update the display album art."""
        raise NotImplementedError

    def update_overlay(self, shuffle, repeat, state, volume,
                       progress, elapsed, title, album, artist):
        """Update the display transport information."""
        # pylint: disable=too-many-arguments
        self._shuffle = shuffle
        self._repeat = repeat
        self._state = state
        self._volume = volume
        self._progress = progress
        self._elapsed = elapsed
        self._title = title
        self._album = album
        self._artist = artist

    def redraw(self):
        """Redraw the display."""
        raise NotImplementedError

    def add_args(argparse):  # pylint: disable=no-self-argument
        """Expand argparse instance with display-specific args."""


class DisplayDummy(Display):
    """Dummy display output. Does nothing."""
    def update_album_art(self, input_file):
        """Ignore display album art. This is a dummy."""

    def redraw(self):
        """Ignore redraw calls. This is a dummy."""


class DisplayMPV(Display):
    """Display using MPV, playing album art as if it were media."""
    def __init__(self, args):
        """Initialise an MPV display."""
        import mpv  # pylint: disable=import-outside-toplevel
        Display.__init__(self, args)
        self._player = mpv.MPV(start_event_thread=False)
        self._player["force-window"] = "immediate"
        self._player["keep-open"] = "yes"
        self._player["geometry"] = f"{self._size}x{self._size}"
        self._player["autofit"] = f"{self._size}x{self._size}"
        self._player["title"] = "bum"
        self._art = None

    def update_album_art(self, input_file):
        """Update album art."""
        self._art = str(input_file)

    def redraw(self):
        """Display album art using MPV"""
        if self._art is not None:
            self._player.player(self._art)
