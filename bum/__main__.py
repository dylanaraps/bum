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
import sys

from . import display
from . import song

from .__init__ import __version__


def get_args():
    """Get the script arguments."""
    description = "bum - Download and display album art \
                   for mpd tracks."
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("--size", metavar="\"px\"",
                     help="what size to display the album art in.",
                     default=250)

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

    return arg.parse_args()


def process_args(args):
    """Process the arguments."""
    if args.version:
        print(f"bum {__version__}")
        sys.exit(0)


def main():
    """Main script function."""
    args = get_args()
    process_args(args)

    if not args.no_display:
        disp = display.init(args.size)

    client = song.init(args.port, args.server)

    while True:
        song.get_art(args.cache_dir, args.size, client)
        if not args.no_display:
            display.launch(disp, args.cache_dir / "current.jpg")

        client.send_idle()

        if client.fetch_idle(["player"]):
            print("album: Received player event from mpd. Swapping cover art.")
            continue


if __name__ == "__main__":
    main()
