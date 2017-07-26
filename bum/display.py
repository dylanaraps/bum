"""
Display related functions.
"""
import mpv


def init():
    """Initialize mpv."""
    player = mpv.MPV(start_event_thread=False)
    player["force-window"] = "immediate"
    player["keep-open"] = "yes"
    player["image-display-duration"] = "inf"
    player["geometry"] = "250x250-64-64"
    player["autofit"] = "250x250"
    player["title"] = "bum"

    return player


def launch(player, input_file):
    """Open mpv."""
    player.play(input_file)
