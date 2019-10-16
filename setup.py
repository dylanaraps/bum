"""pidi - setup.py"""
import sys
import setuptools

try:
    import pidi
except (ImportError, SyntaxError):
    print("error: pidi requires Python 3.6 or greater.")
    sys.exit(1)


try:
    import pypandoc
    LONG_DESC = pypandoc.convert("README.md", "rst")
except(IOError, ImportError, RuntimeError):
    LONG_DESC = open('README.md').read()


VERSION = pidi.__version__
DOWNLOAD = "https://github.com/pimoroni/pidi/archive/%s.tar.gz" % VERSION


setuptools.setup(
    name="pidi",
    version=VERSION,
    author="Phil Howard",
    author_email="phil@pimoroni.com",
    description="Download and display album art for mpd tracks.",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/pimoroni/pidi",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pidi"],
    entry_points={
        "console_scripts": ["pidi=pidi.__main__:main"]
    },
    install_requires=[
        "musicbrainzngs",
        "python-mpd2",
    ],
    extras_require={
        'mpv': ["python-mpv"],
        'tk': ["tk", "pil"],
    },
    python_requires=">=3.6",
    test_suite="tests",
    include_package_data=True
)
