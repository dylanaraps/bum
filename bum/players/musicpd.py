
"""
mpd.
"""
import os
import mpd


def init(port=6600):
    """Initialize mpd."""
    client = mpd.MPDClient()

    try:
        client.connect("localhost", port)
        return client

    except ConnectionRefusedError:
        print("error: Connection refused to mpd/mopidy.")
        os._exit(1)  # pylint: disable=W0212


def get_song(client):
    """Get current song."""
    return client.currentsong()
