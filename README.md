# 🎵 bum

[![PyPI](https://img.shields.io/pypi/v/bum.svg)](https://pypi.python.org/pypi/bum/) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md) [![Build Status](https://travis-ci.org/dylanaraps/bum.svg?branch=master)](https://travis-ci.org/dylanaraps/bum)

`bum` is a daemon that downloads album art for songs playing in `mpd`/`mopidy` and displays them in a little window. `bum` doesn't loop on a timer, instead it waits for `mpd`/`mopidy` to send a `player` event. When it receives a `player` event it wakes up and downloads album art for the current playing track. This makes `bum` lightweight and makes it idle at `~0%` CPU usage.

`bum` uses [musicbrainz](https://musicbrainz.org/) to source and download cover art, if an album is missing it's cover art you can easily create an account and fill in the data yourself. `bum` outputs a `release-id` which you can use to find the exact entry on musicbrainz.

Note: `bum` is meant to be used with files that don't have embedded album art (`mopidy-spotify`).


![showcase](http://i.imgur.com/uKomDoL.gif)


## Dependencies

- `python 3.6+`
- `python-mpv`
- `python-mpd2`
- `musicbrainzngs`


## Installation

```py
pip3 install --user bum
```


## Usage

```sh
usage: bum [-h] [--size "px"] [--cache_dir "/path/to/dir"] [--version]

bum - Download and display album art for mpd tracks.

optional arguments:
  -h, --help            show this help message and exit
  --size "px"           what size to display the album art in.
  --cache_dir "/path/to/dir"
                        Where to store the downloaded cover art.
  --version             Print "bum" version.
```
