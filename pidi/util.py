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
    """Return binary version of default album art."""
    return base64.b64decode("""
iVBORw0KGgoAAAANSUhEUgAAAOYAAADmAQMAAAD7pGv4AAAABlBMVEX///8AAABVwtN+AAAChUlE
QVRYw6XZsW0jMRCFYRoXTMYKWIRClsXQ4WXX1lVwNbAQB5YXgiBpZ77gRNiAtZS5/HfJmTePrb3R
Luyb6F1toHe3Xnd+/G1R9/76/fNTtTj+vWr9uHXVxjHtqs3bb4XbALxv965wWw18sJbAcR+gwq2B
x33iFW4NvB5GyHFL4NtsA7glcDwNkeNWwONp6jluBbxexshwC+D7XAO4BXCcBslwc+BxmnyGmwOv
ZJSW3K0DNwV+oEyAIx0mu9kGbgY8i7/P3x/ATYCf5hnATYCjHOh8qw3cM/DEp9dvD+CegF9mGcA9
fQwO1TmNQYRJ/MVHt/XYTy8lml7o04XgUulcZoNLdHJ5L26NrW2VbLpo2rAPl4KhoDOMDIagyfC1
GPq2wmYaVKMpIN8vBkN9Z5oYTDGT6WkxtW2lxSJpRlPCvV0OpvJOGTAoISblx6J02ZI9pSiKJkF1
dASlWqfMG5SIk/JyUZpuyVqI3mgSzNeuoBTvlPGDJYAKhAncH+CN3g7cKzBwr8B/VPB8/GM99MXe
zzd6v/5/Viby0/CT9FvwG/Tb58rxqvOK9Wr3TvEu8w717mZkcFRxRHI0cyR0FHUEdvRm5HfWcMZx
tnKmc5Z0hnV2Zma3KrCisBqxkrEKsoKy+qJys+qzYrTatFK1yrVCtrqmMreqd0XgasKViKsYV0Cu
nlh5uWpzxedq0ZWmq1RXuK6OWVm7KndFbzfAToJdCDsYdj/onNh1sWNjt8dOkV0mO1R2t+iM2VWz
I2c3z06gXUQ7kIvJayvx2TW142q31k6vXWI7zIviZEvY2BW3o2433k6+TwF8grAoPreEq089fGLi
0xaf1PiUxydEF/Re2hvtG6k8p7n4F+LQAAAAAElFTkSuQmCC
""")
