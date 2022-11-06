import os
# from MLibLogging import MLogger
from dotenv import load_dotenv

import MLibSpotify.MLibSpotify.Utilities as Util
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

    TestPlaylist = SpotifyPlaylist(playlist_id=TestPlaylistId,
                                   access_token=os.getenv("ACCESS_TOKEN"))

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
    global TestPlaylist

    original_num_tracks = len(TestPlaylist.GetAllTracks())
    TestPlaylist.AddTracks(TestTrackIds)
    new_num_tracks = len(TestPlaylist.GetAllTracks(force_refresh=True))

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


# endregion

# region Run tests

# __logger.Info('Starting Spotify Tests')
print('Starting spotify tests')
AuthorizationTest()
GetTracksTest()
TrackAddTest()
GetUrlTest()

# endregion

# region Refresh access token

# Util.GetAuthorizationCode()
# Util.GetAccessToken()
# Util.RefreshAccessToken()

# endregion
