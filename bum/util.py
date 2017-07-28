"""
Util functions.
"""
import pathlib


def bytes_to_file(input_data, output_file):
    """Save bytes to a file."""
    pathlib.Path(output_file.parent).mkdir(parents=True, exist_ok=True)

    with open(output_file, "wb") as file:
        file.write(input_data)


def signal_usr1(sig, frame):
    """Handle 'pkill -USR1 bum'."""
    print("signal: Recieved SUGUSR1, swapping album art.")

    # Args are required when using signal, but we don't need them.
    del sig, frame
