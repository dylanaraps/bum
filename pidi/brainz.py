"""
Musicbrainz related functions.
"""
import time
import musicbrainzngs as mus

from .__init__ import __version__


def init():
    """Initialize musicbrainz."""
    mus.set_useragent("python-pidi: A cover art daemon.",
                      __version__,
                      "https://github.com/pimoroni/pidi")


def get_cover(song, size=250, retry_delay=5, retries=5):
    """Download the cover art."""
    artist = song.get('artist')
    title = song.get('title')
    album = song.get('album', title)
    try:
        data = mus.search_releases(artist=artist,
                                   release=album,
                                   limit=1)
        release_id = data["release-list"][0]["release-group"]["id"]
        print("album: Using release-id: {id}".format(data['release-list'][0]['id']))

        return mus.get_release_group_image_front(release_id, size=size)

    except mus.NetworkError:
        if retries == 0:
            raise mus.NetworkError("Failure connecting to MusicBrainz.org")
        print("warning: Retrying download. {retries} retries left!".format(retires=retries))
        time.sleep(retry_delay)
        get_cover(song, size, retries=retries - 1)

    except mus.ResponseError:
        print("error: Couldn't find album art for",
              "{artist} - {album}".format(artist=artist, album=album))
