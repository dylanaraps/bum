"""
Display Output Classes.
"""
import time
import math


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


class DisplayST7789(DisplayPIL):
    def __init__(self, args):
        from ST7789 import ST7789, BG_SPI_CS_FRONT
        DisplayPIL.__init__(self, args)
        self._st7789 = ST7789(
            rotation=args.rotation,
            port=args.spi_port,
            cs=args.spi_chip_select_pin,
            dc=args.spi_data_command_pin,
            backlight=args.backlight_pin,
            spi_speed_hz=args.spi_speed_mhz * 1000 * 1000
        )
        self._st7789.begin()

    def redraw(self):
        DisplayPIL.redraw(self)
        self._st7789.display(self._output_image)

    def add_args(argparse):
        """Add supplemental arguments for ST7789."""
        argparse.add_argument("--rotation",
                              help="Rotation in degrees (Default: 90)",
                              type=int, default=90, choices=[0, 90, 180, 270])
        argparse.add_argument("--spi-port",
                              help="SPI port (Default 0)",
                              type=int, default=0, choices=[0,1])
        argparse.add_argument("--spi-chip-select-pin",
                              help="SPI chip select (Default 1)",
                              type=int, default=1, choices=[0, 1])
        argparse.add_argument("--spi-data-command-pin",
                              help="SPI data/command pin (Default 9)",
                              type=int, default=9)
        argparse.add_argument("--spi-speed-mhz",
                              help="SPI speed in Mhz (Default 80)",
                              type=int, default=90)
        argparse.add_argument("--backlight-pin",
                              help="ST7789 backlight pin (Default 19)",
                              type=int, default=19)



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


class DisplayTK(DisplayPIL):
    def __init__(self, args):
        global ImageTk, tkinter

        DisplayPIL.__init__(self, args)

        from PIL import ImageTk
        import tkinter

        self._root = tkinter.Tk()
        self._root.geometry(f'{self._size}x{self._size}')
        self._root.resizable(False, False)

    def redraw(self):
        DisplayPIL.redraw(self)

        self._root.title(f"{self._title} - {self._artist}, {self._album}")

        imagetk = ImageTk.PhotoImage(self._output_image)
        label_image = tkinter.Label(self._root, image=imagetk)
        label_image.place(x=0, y=0, width=self._size, height=self._size)

        self._root.update()
