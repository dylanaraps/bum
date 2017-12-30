"""
Players that support playerctl.
"""
import gi
gi.require_version('Playerctl', '1.0')

from gi.repository import Playerctl


def init():
    """Initialize player."""
    return Playerctl.Player()


def get_song(client):
    """Get current song."""
    return {"artist": client.get_artist(),
            "title": client.get_title(),
            "album": client.get_album()}
