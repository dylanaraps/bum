"""
Display Output Classes.
"""


class Display():
    def __init__(self, size):
        pass

    def update_album_art(self, input_file):
        pass

    def update_overlay(self, shuffle, repeat, state, volume, progress, title, album, artist):
        pass

    def redraw(self):
        pass


class DisplayDummy(Display):
    pass


class DisplayMPV(Display):
    def __init__(self, size=240):
        global mpv
        import mpv
        self._player = mpv.MPV(start_event_thread=False)
        self._player["force-window"] = "immediate"
        self._player["keep-open"] = "yes"
        self._player["geometry"] = f"{size}x{size}"
        self._player["autofit"] = f"{size}x{size}"
        self._player["title"] = "bum"

    def update_album_art(self, input_file):
        self._art = str(input_file)

    def redraw(self):
        self._player.player(self._art)


class DisplayTK(Display):
    def __init__(self, size=240):
        global ImageTk, Image, ImageDraw, ImageFont, ConnectionIII, tkinter
        from PIL import ImageTk, Image, ImageDraw, ImageFont
        from fonts.otf import ConnectionIII
        import tkinter

        Display.__init__(self, size)
        self._size = size
        self._root = tkinter.Tk()
        self._font = ImageFont.truetype(ConnectionIII, 20)
        self._root.geometry(f'{size}x{size}')
        self._root.resizable(False, False)
        self._image = Image.new('RGBA', (size, size), (0, 0, 0))
        self._overlay = Image.new('RGBA', (size, size))
        self._draw = ImageDraw.Draw(self._overlay, 'RGBA')
        self._draw.fontmode = '1'

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
        new = Image.open(input_file).resize((self._size - 10, self._size - 10))
        self._image.paste(new, (5, 5))

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
        self._root.title(f"{self._title} - {self._artist}, {self._album}")

        # Clear overlay
        self._draw.rectangle((0, 0, self._size, self._size), (0, 0, 0, 0))

        bar_width = int(self._size * self._progress)
        self._draw.rectangle((0, self._size - 90, bar_width, self._size - 80), (255, 0, 0, 200))

        self._draw.rectangle((0, self._size - 80, self._size, self._size), (0, 0, 0, 200))

        # Song Title
        text_w, text_h = self._font.getsize(self._title)
        self._draw.text(((self._size / 2) - (text_w / 2), (self._size-80) + 10), self._title, font=self._font)

        # Album
        text_w, text_h = self._font.getsize(self._album)
        self._draw.text(((self._size / 2) - (text_w / 2), (self._size-80) + 30), self._album, font=self._font)

        # Artist
        text_w, text_h = self._font.getsize(self._artist)
        self._draw.text(((self._size / 2) - (text_w / 2), (self._size-80) + 50), self._artist, font=self._font)

        output_image = Image.alpha_composite(self._image, self._overlay)

        imagetk = ImageTk.PhotoImage(output_image)
        label_image = tkinter.Label(self._root, image=imagetk)
        label_image.place(x=0, y=0, width=self._size, height=self._size)

        self._root.update()
