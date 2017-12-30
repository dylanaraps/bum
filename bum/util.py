"""
Util functions.
"""
import pathlib
import subprocess


def bytes_to_file(input_data, output_file):
    """Save bytes to a file."""
    pathlib.Path(output_file.parent).mkdir(parents=True, exist_ok=True)

    with open(output_file, "wb") as file:
        file.write(input_data)


def get_pid(name):
    """Get PID by process name."""
    pid = subprocess.run(["pidof", name], stdout=subprocess.PIPE)
    return pid.stdout
