"""
Musicbrainz related functions.
"""
import musicbrainzngs as mus

from .__init__ import __version__


def init():
    """Initialize musicbrainz."""
    mus.set_useragent("python-bum: A cover art daemon.",
                      __version__,
                      "https://github.com/dylanaraps/bum")


def get_cover(song, size=250):
    """Download the cover art."""
    try:
        data = mus.search_releases(artist=song["artist"],
                                   release=song["album"],
                                   limit=1)
        release_id = data["release-list"][0]["release-group"]["id"]
        print(f"album: Using release-id: {data['release-list'][0]['id']}")

        return mus.get_release_group_image_front(release_id, size=size)

    except mus.NetworkError:
        get_cover(song, size)

    except mus.ResponseError:
        print("error: Couldn't find album art for",
              f"{song['artist']} - {song['album']}")
