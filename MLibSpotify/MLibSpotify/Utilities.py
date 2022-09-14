import spotipy
import re

TrackApiBase = 'https://api.spotify.com/v1/tracks/'


def ExtractLinks(message_text):
    # TODO: Update to accept multiple Urls

    # Example message:
    # Here's more: https://open.spotify.com/track/0irYSFrgXf2OH1F5NAdK6I?si=0e85a2bb98714998

    return [re.search("(?P<url>https?://[^\s]+)", message_text).group("url")]


def GetUri(spotify_link):
    # Example link:
    # https://open.spotify.com/track/{track_uri}?si=6da81c5d48394b23
    uri = spotify_link.split("/track/", 1)[1]
    uri = uri.split("?", 1)[0]

    return f'{TrackApiBase}{uri}'
