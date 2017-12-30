
"""
cmus.
"""
from pycmus import remote


def init(port=3000):
    """Initialize mpd."""
    return remote.PyCmus(port=port)


def get_song(client):
    """Get current song."""
    status = client.get_status_dict()
    return {**status["tag"]}
