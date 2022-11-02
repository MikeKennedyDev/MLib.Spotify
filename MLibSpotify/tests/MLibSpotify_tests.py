import os
from bs4 import BeautifulSoup

import requests
# from MLibLogging import MLogger
from dotenv import load_dotenv

import MLibSpotify.MLibSpotify.Utilities as Util
from MLibSpotify.MLibSpotify.SpotifyPlaylist import AuthorizationValues
from MLibSpotify.MLibSpotify.SpotifyPlaylist import SpotifyPlaylist

load_dotenv()

# region Fields

TestPlaylist = None
TestPlaylistId = '2UmDYQxgIDaKikeG53Ffd5'
TestTrackIds = ['56rgqDNRIqKq0qIMdu7r4r', '1rWzYSHyZ5BiI4DnDRCwy7']
TestTrackUri = 'https://api.spotify.com/v1/tracks/0irYSFrgXf2OH1F5NAdK6I'


# __logger = MLogger.MLogger('MLibSpotify')


# endregion

# region Test Methods

def AuthorizationTest():
    global TestPlaylist

    token = "BQD06Kp4l2cTgAzcZ3kfl2mrYRubd_92TEHegFr8LzzDbu_hYAbV7IgTX9OEO2AMGz_8IT378ApyH2AVEeTL7ClkiA3nG8Itu-QPFBt_gbbDTqMKe39fMvujY7qA4gM9QZmTfIBVwRsFp7C9gM71rVMvHdzqbhu0DM_7jTCFB30HHJXPClhXgwc5EdAREaH_gRmmncgnnD8f8K3WTT74v_mNCT4lKWpOoFozE27C6bw"
    TestPlaylist = SpotifyPlaylist(auth_token=token, playlist_id=TestPlaylistId)

    assert TestPlaylist is not None
    # __logger.Debug('AuthorizationTest success')
    print('AuthorizationTest success')


def GetTracksTest():
    global TestPlaylist
    all_tracks = TestPlaylist.GetAllTracks(force_refresh=True)

    assert all_tracks is not None
    # __logger.Debug('GetTracks test success')
    print('GetTracks test success')


def TrackAddTest():
    auth = AuthorizationValues(client_id=os.getenv("CLIENT_ID"),
                               client_secret=os.getenv("CLIENT_SECRET"),
                               scope='playlist-read-collaborative playlist-modify-public')
    playlist = SpotifyPlaylist(auth, playlist_id=TestPlaylistId)

    original_num_tracks = len(playlist.GetAllTracks())
    playlist.AddTracks(TestTrackIds)
    new_num_tracks = len(playlist.GetAllTracks(force_refresh=True))

    assert new_num_tracks == (original_num_tracks + len(TestTrackIds))
    # __logger.Debug(f'{len(TestTrackIds)} tracks added successfully')
    print(f'{len(TestTrackIds)} tracks added successfully')


def GetUrlTest():
    # Todo: build test
    spotify_api = f'https://api.spotify.com/v1/tracks/{TestTrackIds[0]}'
    message = "Here's a link https://open.spotify.com/track/0irYSFrgXf2OH1F5NAdK6I?si=0e85a2bb98714998"
    url = 'https://open.spotify.com/track/0irYSFrgXf2OH1F5NAdK6I?si=0e85a2bb98714998'
    urls = Util.GetSpotifyLinks(message)
    # __logger.Info(f'Urls retrieved from message: {message}')
    print(f'Urls retrieved from message: {message}')
    for url in urls:
        print(f"-'{url}'")
        # __logger.Info(f"-'{url}'")

    return


def GetNewAuthToken():
    # Send get request to /authorize
    client_id = os.getenv("CLIENT_ID")
    print(f'using client_id: {client_id}')

    redirect_uri = os.getenv("RedirectUri")
    print(f'using redirect_uri: {redirect_uri}')

    scope = 'playlist-read-collaborative playlist-modify-public'

    endpoint = 'https://accounts.spotify.com/authorize?'
    headers = {'client_id': client_id,
               'response_type': 'code',
               'redirect_uri': redirect_uri,
               'scope': scope}

    response = requests.get(endpoint, headers=headers)
    parsed_response = BeautifulSoup(response.content)

    print(parsed_response)

    return


# endregion

# region Run tests

# __logger.Info('Starting Spotify Tests')
print('Starting spotify tests')
# AuthorizationTest()
# GetTracksTest()
# TrackAddTest()
# GetUrlTest()

# endregion

GetNewAuthToken()
