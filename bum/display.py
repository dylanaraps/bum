"""
Display related functions.
"""
import mpv


def init(size=250):
    """Initialize mpv."""
    player = mpv.MPV(start_event_thread=False)
    player["force-window"] = "immediate"
    player["keep-open"] = "yes"
    player["geometry"] = f"{size}x{size}"
    player["autofit"] = f"{size}x{size}"
    player["title"] = "bum"

    return player


def launch(player, input_file):
    """Open mpv."""
    player.play(str(input_file))
