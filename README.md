![bum](https://imgur.com/MM9xunG.png "🎵 bum")  

[![PyPI](https://img.shields.io/pypi/v/bum.svg)](https://pypi.python.org/pypi/bum/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Build Status](https://travis-ci.org/dylanaraps/bum.svg?branch=master)](https://travis-ci.org/dylanaraps/bum)
[![Donate](https://img.shields.io/badge/donate-patreon-yellow.svg)](https://www.patreon.com/dyla)

`bum` is a daemon that downloads album art for songs playing in `mpd`/`mopidy` and displays them in a little window. the window can be spawned at any user specified position.  `bum` doesn't loop on a timer, instead it waits for `mpd`/`mopidy` to send a `player` event. When it receives a `player` event it wakes up and downloads album art for the current playing track. This makes `bum` lightweight and makes it idle at `~0%` CPU usage.

`bum` uses [musicbrainz](https://musicbrainz.org/) to source and download cover art, if an album is missing it's cover art you can easily create an account and fill in the data yourself. `bum` outputs a `release-id` which you can use to find the exact entry on musicbrainz.

Note: `bum` is meant to be used with files that don't have embedded album art (`mopidy-spotify`).  

![showcase](http://i.imgur.com/uKomDoL.gif)

## New Feature

now you can specify the exact position for spawning the album art window at , using the `--position=` argument.  

![position](https://github.com/yedhink/bum/blob/displayLocation/logo/bumPosition.gif)  

refer to this graph for getting a better idea on how to position. the arrows indicate in which direction the window would be pushed.  
```bash

                             | +y |
                             |    V
                             |
                             |
                             |
                             |
                             |
                             |
+x --->                      |                      <---  -x
_____________________________|______________________________
                             |+0+0(default)
                             |
                             |
                             |
                             |
                             |
                             |
                             |
                             |    ^
                             | -y |

```

## Dependencies

- `python 3.6+`
- `python-mpv`
- `python-mpd2`
- `musicbrainzngs`


## Installation

```sh
pip3 install --user bum
```


## Usage

```sh
usage: bum [-h] [--size "px"] [--position "=x+y"] [--cache_dir "/path/to/dir"]
           [--version] [--port PORT] [--server SERVER]

bum - Download and display album art for mpd tracks.

optional arguments:
  -h, --help            show this help message and exit
  --size "px"           what size to display the album art in.
  --position "=x+y"     what position to display the album art at. example:
                        bum --position=-10+10
  --cache_dir "/path/to/dir"
                        Where to store the downloaded cover art.
  --version             Print "bum" version.
  --port PORT           Use a custom mpd port.
  --server SERVER       Use a remote server instead of localhost.
```


## Donate

Donations will allow the creator of the project to spend more time working on `bum`.

If you like `bum` and want to give back in some way you can donate here:

**https://patreon.com/dyla**
