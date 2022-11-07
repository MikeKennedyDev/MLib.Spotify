import base64
import os
import re
import webbrowser
from urllib.parse import urlencode

import requests

TrackApiBase = 'https://api.spotify.com/v1/tracks/'


def GetPlaylistEndpoint(playlist_id):
    return f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'


def GetAddTracksEndpoint(playlist_id, tracks):
    uris = '%2C'.join([f'spotify%3Atrack%3A{track}' for track in tracks])
    return f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={uris}'


def GetSpotifyLinks(message_text):
    # TODO: Update to accept multiple Urls

    # Example message:
    # Here's more: https://open.spotify.com/track/0irYSFrgXf2OH1F5NAdK6I?si=0e85a2bb98714998

    search_results = re.search("(?P<url>https?://[^\s]+)", message_text)
    if search_results is not None:
        return [search_results.group(('url'))]
    return None


def GetUri(spotify_link):
    print(f'Getting uri from link: {spotify_link}')
    # Example link:
    # https://open.spotify.com/track/{track_uri}?si=6da81c5d48394b23
    uri = spotify_link.split("/track/", 1)[1]
    uri = uri.split("?", 1)[0]
    print(f'track id: {uri}')

    return f'{TrackApiBase}{uri}'


def GetTrackId(spotify_link):
    print(f'Getting id from link: {spotify_link}')
    # Example link:
    # https://open.spotify.com/track/{track_uri}?si=6da81c5d48394b23
    Id = spotify_link.split("/track/", 1)[1]
    Id = Id.split("?", 1)[0]
    print(f'track id: {Id}')

    return Id


def EncodeAuthorization(client_id, client_secret):
    encoded_id = client_id.encode()
    encoded_secret = client_secret.encode()

    encoded_creds = base64.b64encode(encoded_id + b':' + encoded_secret).decode("utf-8")

    return f'Basic {encoded_creds}'


def GetAccessToken(RefreshToken=None):
    request_headers = {
        "Authorization": EncodeAuthorization(client_id=os.getenv("CLIENT_ID"),
                                             client_secret=os.getenv("CLIENT_SECRET")),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_body = {
        "grant_type": "authorization_code",
        "code": os.getenv("AUTHORIZATION_CODE"),
        "redirect_uri": os.getenv("REDIRECT_URI")
    }

    response = requests.post("https://accounts.spotify.com/api/token",
                             headers=request_headers,
                             data=request_body)
    print(response)
    print(response.content)
    return response.json()['access_token']


def RefreshAccessToken():
    request_headers = {
        "Authorization": EncodeAuthorization(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_body = {
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("REFRESH_TOKEN")
    }

    response = requests.post("https://accounts.spotify.com/api/token",
                             headers=request_headers,
                             data=request_body)
    print(response)
    print(response.content)
    return response.json()['access_token']


def GetAuthorizationCode():
    # Send get request to /authorize
    client_id = os.getenv("CLIENT_ID")
    redirect_uri = os.getenv("REDIRECT_URI")
    scope = 'playlist-read-collaborative playlist-modify-public'

    auth_url = 'https://accounts.spotify.com/authorize?'
    headers = {"client_id": client_id,
               "response_type": "code",
               "redirect_uri": redirect_uri,
               "scope": scope
               }

    # Code is returned in web browser here
    webbrowser.open(auth_url + urlencode(headers))

    return
