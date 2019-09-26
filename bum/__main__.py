"""
'||
 || ...  ... ...  .. .. ..
 ||'  ||  ||  ||   || || ||
 ||    |  ||  ||   || || ||
 '|...'   '|..'|. .|| || ||.

Created by Dylan Araps
"""
import argparse
import pathlib
import time

from . import display
from .song import Song

from .__init__ import __version__


display_types = {
    'dummy': display.DisplayDummy,
    'tk': display.DisplayTK,
    'mpv': display.DisplayMPV
}


def get_args():
    """Get the script arguments."""
    description = "bum - Download and display album art \
                   for mpd tracks."
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("--update-interval", metavar="\"i\"",
                     help="overlay update interval in seconds.",
                     default=2)

    arg.add_argument("--size", metavar="\"px\"",
                     help="what size to display the album art in.",
                     default=240)

    arg.add_argument("--cache_dir", metavar="\"/path/to/dir\"",
                     help="Where to store the downloaded cover art.",
                     default=pathlib.Path.home() / ".cache/bum")

    arg.add_argument("--version", action="store_true",
                     help="Print \"bum\" version.")

    arg.add_argument("--port",
                     help="Use a custom mpd port.",
                     default=6600)

    arg.add_argument("--server",
                     help="Use a remote server instead of localhost.",
                     default="localhost")

    arg.add_argument("--no_display",
                     action="store_true",
                     help="Only download album art, don't display.")

    arg.add_argument("--display", choices=display_types.keys(),
                     help="Display class to use.",
                     default='dummy')

    return arg.parse_args()


def process_args(args):
    """Process the arguments."""
    if args.version:
        print(f"bum {__version__}")
        exit(0)


def main():
    """Main script function."""
    display = None
    args = get_args()
    process_args(args)

    if args.no_display:
        print("Warning --no_display overrides --display option!")
        args.display = 'dummy'

    display = display_types[args.display](args.size)

    client = Song(args.port, args.server)

    last_track = ''
    last_update = 0

    while True:
        if client.update_pending() or time.time() - last_update > args.update_interval:
            status = client.status()
            currentsong = client.currentsong()

            current_track = f"{currentsong['title']} - {currentsong['artist']}, {currentsong['album']}"
            if current_track != last_track:
                client.get_art(args.cache_dir, args.size)
                display.update_album_art(args.cache_dir / "current.jpg")
                last_track = current_track

            display.update_overlay(
                shuffle=status['random'] == '1',
                repeat=status['repeat'] == '1',
                state=status['state'],
                volume=int(status['volume']),
                progress=float(status['elapsed']) / float(currentsong['time']),
                title=currentsong['title'],
                album=currentsong['album'],
                artist=currentsong['artist']
            )

            last_update = time.time()

        display.redraw()

        time.sleep(1.0 / 60.0)


if __name__ == "__main__":
    main()
