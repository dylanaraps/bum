"""
Display Output Classes.
"""
import time
import math
from pkg_resources import iter_entry_points


def get_display_types():
    display_types = {
        'dummy': DisplayDummy,
        'mpv': DisplayMPV,
    }

    for ep in iter_entry_points("bum_plugin_display"):
        try:
            plugin = ep.load()
            display_types[plugin.option_name] = plugin
        except (ModuleNotFoundError, ImportError) as e:
            print(f"Error loading display plugin {ep}: {e}")

    return display_types


class Display():
    def __init__(self, args=None):
        self._size = args.size
        self._title = ''
        self._shuffle = False
        self._repeat = False
        self._state = ''
        self._volume = 0
        self._progress = 0

        self._title = ''
        self._album = ''
        self._artist = ''

    def update_album_art(self, input_file):
        pass

    def update_overlay(self, shuffle, repeat, state, volume, progress, title, album, artist):
        self._shuffle = shuffle
        self._repeat = repeat
        self._state = state
        self._volume = volume
        self._progress = progress
        self._title = title
        self._album = album
        self._artist = artist

    def redraw(self):
        pass

    def add_args(argparse):
        pass


class DisplayPIL(Display):
    """Base class for PIL-based image displays."""
    def __init__(self, args=None):
        global Image, ImageDraw, ImageFont, ConnectionIII

        Display.__init__(self, args)

        from fonts.otf import ConnectionIII
        from PIL import ImageTk, Image, ImageDraw, ImageFont
        
        self._font = ImageFont.truetype(ConnectionIII, 20)
        self._image = Image.new('RGBA', (self._size, self._size), (0, 0, 0))
        self._overlay = Image.new('RGBA', (self._size, self._size))
        self._draw = ImageDraw.Draw(self._overlay, 'RGBA')
        self._draw.fontmode = '1'
        self._output_image = None
        self._last_change = time.time()

    def update_album_art(self, input_file):
        Display.update_album_art(self, input_file)
        new = Image.open(input_file).resize((self._size - 10, self._size - 10))
        self._image.paste(new, (5, 5))
        self._last_change = time.time()

    def redraw(self):
        scroll_offset = 0
        if time.time() - self._last_change > 1:
            t = time.time() - self._last_change - 1
            scroll_offset = math.sin(t)
            scroll_offset = min(0.75, scroll_offset)
            scroll_offset = max(-0.75, scroll_offset)
            scroll_offset *= 1.333

        # Clear overlay
        self._draw.rectangle((0, 0, self._size, self._size), (0, 0, 0, 0))

        bar_width = int(self._size * self._progress)
        self._draw.rectangle((0, self._size - 90, bar_width, self._size - 80), (255, 0, 0, 200))

        self._draw.rectangle((0, self._size - 80, self._size, self._size), (0, 0, 0, 200))

        # Song Title
        text_w, text_h = self._font.getsize(self._title)
        text_offset_left = 0
        if text_w > self._size:
            text_offset_left = scroll_offset * ((text_w - self._size) / 2.0)
            text_offset_left += scroll_offset * 10.0

        self._draw.text(((self._size / 2) - (text_w / 2) + text_offset_left, (self._size - 80) + 10), self._title, font=self._font)

        # Album
        text_w, text_h = self._font.getsize(self._album)
        text_offset_left = 0
        if text_w > self._size:
            text_offset_left = scroll_offset * ((text_w - self._size) / 2.0)
            text_offset_left += scroll_offset * 10.0

        self._draw.text(((self._size / 2) - (text_w / 2) + text_offset_left, (self._size - 80) + 30), self._album, font=self._font)

        # Artist
        text_w, text_h = self._font.getsize(self._artist)
        text_offset_left = 0
        if text_w > self._size:
            text_offset_left = scroll_offset * ((text_w - self._size) / 2.0)
            text_offset_left += scroll_offset * 10.0

        self._draw.text(((self._size / 2) - (text_w / 2) + text_offset_left, (self._size - 80) + 50), self._artist, font=self._font)

        self._output_image = Image.alpha_composite(self._image, self._overlay)


class DisplayDummy(Display):
    pass


class DisplayMPV(Display):
    def __init__(self, args):
        global mpv
        import mpv
        Display.__init__(self, args)
        self._player = mpv.MPV(start_event_thread=False)
        self._player["force-window"] = "immediate"
        self._player["keep-open"] = "yes"
        self._player["geometry"] = f"{self._size}x{self._size}"
        self._player["autofit"] = f"{self._size}x{self._size}"
        self._player["title"] = "bum"

    def update_album_art(self, input_file):
        self._art = str(input_file)

    def redraw(self):
        self._player.player(self._art)
