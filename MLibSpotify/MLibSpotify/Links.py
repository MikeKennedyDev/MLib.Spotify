import re


def GetSpotifyPlaylistUrl(playlist_id):
    return f"https://open.spotify.com/playlist/{playlist_id}"


def GetSpotifyLinks(message_text):
    # TODO: Update to accept multiple Urls

    # Example message:
    # Here's more: https://open.spotify.com/track/0irYSFrgXf2OH1F5NAdK6I?si=0e85a2bb98714998

    if 'track' not in message_text:
        return None

    search_results = re.search("(?P<url>https?://[^\s]+)", message_text)
    if search_results is not None:
        return [search_results.group('url')]
    return None


def GetTrackId(spotify_link):
    # Example link:
    # https://open.spotify.com/track/{track_id}?si=6da81c5d48394b23

    print(f'Getting track id from link: {spotify_link}')
    Id = spotify_link.split("/track/", 1)[1]
    Id = Id.split("?", 1)[0]

    return Id


def GetPlaylistId(playlist_link):
    # Example url:
    # https://open.spotify.com/playlist/{playlist_id}?si=61478f711eaa48ab

    print(f'Getting playlist id from link: {playlist_link}')
    Id = playlist_link.split("/playlist/", 1)[1]
    Id = Id.split("?", 1)[0]

    return Id
