# 🎵 bum

`bum` is a daemon that downloads album art for songs playing in `mpd` and displays them in a little window. `bum` doesn't loop on a timer, instead you can send it `SIGUSR1` to get it to download album art for the current playing track. This makes `bum` lightweight and makes it idle at `0%` cpu usage.

Note: `bum` is meant to be used with files that don't have embedded album art (`mopidy-spotify`).

![showcase](http://i.imgur.com/SIC0Ii3.gif)


## Dependencies

- `python 3.6+`
- `python-mpv`
- `musicbrainzngs`
- `mpc`


## Installation

```py
pip install bum
```
