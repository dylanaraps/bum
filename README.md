# 🎵 bum

[![PyPI](https://img.shields.io/pypi/v/bum.svg)](https://pypi.python.org/pypi/bum/) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md) [![Build Status](https://travis-ci.org/dylanaraps/bum.svg?branch=master)](https://travis-ci.org/dylanaraps/bum)

`bum` is a daemon that downloads album art for songs playing in `mpd` and displays them in a little window. `bum` doesn't loop on a timer, instead you can send it `SIGUSR1` to make it wake up and download album art for the current playing track. This makes `bum` lightweight and makes it idle at `~0%` CPU usage.

`bum` uses [musicbrainz](https://musicbrainz.org/) to source and download cover art, if an album is missing it's cover art you can easily create an account and fill in the data yourself.

Note: `bum` is meant to be used with files that don't have embedded album art (`mopidy-spotify`).


![showcase](http://i.imgur.com/uKomDoL.gif)


## Dependencies

- `python 3.6+`
- `python-mpv`
- `musicbrainzngs`
- `mpc`


## Installation

```py
pip install bum
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


## Customization

### ncmpcpp

You can configure `ncmpcpp` to send `SIGUSR1` to `bum` on every song change.


```
# .ncmpcpp/config

# Execute bum on song change.
execute_on_song_change = "pkill -USR1 bum"
```

### shell

You can use `mpc idleloop` to send `SIGUSR1` to `bum` on every song change.


```sh
#!/bin/sh
# Wake up bum on song change.
while :; do
    mpc idleloop player | pkill -USR1 bum$
done
```
