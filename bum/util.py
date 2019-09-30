"""
Util functions.
"""
import pathlib
import base64


def bytes_to_file(input_data, output_file):
    """Save bytes to a file."""
    pathlib.Path(output_file.parent).mkdir(parents=True, exist_ok=True)

    with open(output_file, "wb") as file:
        file.write(input_data)


def default_album_art():
    return base64.b64decode("""
iVBORw0KGgoAAAANSUhEUgAAAOYAAADmAQMAAAD7pGv4AAAABGdBTUEAALGPC/xhBQAAAAFzUkdC
AK7OHOkAAAAGUExURf///yIkJdTndBEAAAKFSURBVFjDpdmxbSMxEIVhGhdMxgpYhEKWxdDhZdfW
VXA1sBAHlheCIGlnvuBE2IC1lLn8d8mZN4+tvdEu7JvoXW2gd7ded378bVH3/vr981O1OP69av24
ddXGMe2qzdtvhdsAvG/3rnBbDXywlsBxH6DCrYHHfeIVbg28HkbIcUvg22wDuCVwPA2R41bA42nq
OW4FvF7GyHAL4PtcA7gFcJwGyXBz4HGafIabA69klJbcrQM3BX6gTIAjHSa72QZuBjyLv8/fH8BN
gJ/mGcBNgKMc6HyrDdwz8MSn128P4J6AX2YZwD19DA7VOY1BhEn8xUe39dhPLyWaXujTheBS6Vxm
g0t0cnkvbo2tbZVsumjasA+XgqGgM4wMhqDJ8LUY+rbCZhpUoykg3y8GQ31nmhhMMZPpaTG1baXF
ImlGU8K9XQ6m8k4ZMCghJuXHonTZkj2lKIomQXV0BKVap8wblIiT8nJRmm7JWojeaBLM166gFO+U
8YMlgAqECdwf4I3eDtwrMHCvwH9U8Hz8Yz30xd7PN3q//n9WJvLT8JP0W/Ab9NvnyvGq84r1avdO
8S7zDvXuZmRwVHFEcjRzJHQUdQR29Gbkd9ZwxnG2cqZzlnSGdXZmZrcqsKKwGrGSsQqygrL6onKz
6rNitNq0UrXKtUK2uqYyt6p3ReBqwpWIqxhXQK6eWHm5anPF52rRlaarVFe4ro5ZWbsqd0VvN8BO
gl0IOxh2P+ic2HWxY2O3x06RXSY7VHa36IzZVbMjZzfPTqBdRDuQi8lrK/HZNbXjarfWTq9dYjvM
i+JkS9jYFbejbjfeTr5PAXyCsCg+t4SrTz18YuLTFp/U+JTHJ0QX9F7aG+0bqTynufgX4tAAAAAA
SUVORK5CYII=
""")