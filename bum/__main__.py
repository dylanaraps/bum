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
import sys

from .display import get_display_types
from .client import get_client_types

from .__init__ import __version__


def get_args(display_types, client_types):
    """Get the script arguments."""
    description = "bum - Download and display album art \
                   for mpd tracks."
    arg = argparse.ArgumentParser("bum", description=description)

    arg.add_argument("--update-interval", metavar="\"i\"",
                     help="overlay update interval in seconds.",
                     default=1)

    arg.add_argument("--fps",
                     help="frames per second.",
                     type=int, default=30)

    arg.add_argument("--size", metavar="\"px\"",
                     help="what size to display the album art in.",
                     default=240)

    arg.add_argument("--cache_dir", metavar="\"/path/to/dir\"",
                     help="Where to store the downloaded cover art.",
                     default=pathlib.Path.home() / ".cache/bum",
                     type=pathlib.Path)

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

    arg.add_argument("--client", choices=client_types.keys(),
                     help="Client class to use.",
                     default='mpd')

    # Strip out --help so we can parse_known_args
    # without triggering help text output.
    has_help = False
    try:
        sys.argv.remove('--help')
        has_help = True
    except ValueError:
        pass

    args, _ = arg.parse_known_args()

    # Add display/client specific args into the parser
    display_types[args.display].add_args(arg)

    client_types[args.client].add_args(arg)

    # Add --help back if it was supplied
    if has_help:
        sys.argv.append('--help')

    return arg.parse_args()


def process_args(args):
    """Process the arguments."""
    if args.version:
        print(f"bum {__version__}")
        sys.exit(0)


def main():
    """Main script function."""
    display_types = get_display_types()
    client_types = get_client_types()

    args = get_args(display_types, client_types)
    process_args(args)

    if args.no_display:
        print("Warning --no_display overrides --display option!")
        args.display = 'dummy'

    display = display_types[args.display](args)

    client = client_types[args.client](args.port, args.server)

    last_track = ''
    last_update = 0

    while True:
        if client.update_pending() or time.time() - last_update > float(args.update_interval):
            status = client.status()
            currentsong = client.currentsong()

            if status == {} or currentsong == {}:
                pass  # No status or song info available
            else:
                title = currentsong.get('title', 'Untitled')
                artist = currentsong.get('artist', 'No Artist')
                album = currentsong.get('album', title)
                current_track = f"{title} - {artist}, {album}"
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
                    elapsed=float(status['elapsed']),
                    title=title,
                    album=album,
                    artist=artist
                )

                last_update = time.time()

        display.redraw()

        time.sleep(1.0 / args.fps)


if __name__ == "__main__":
    main()
