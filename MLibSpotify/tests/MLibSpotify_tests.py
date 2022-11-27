import os
from dotenv import load_dotenv

import MLibSpotify.Links
import Utilities as Util
from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist, GetAllUserPlaylists

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
                                   client_id=os.getenv("CLIENT_ID"),
                                   client_secret=os.getenv("CLIENT_SECRET"),
                                   refresh_token=os.getenv("REFRESH_TOKEN"))

    assert TestPlaylist is not None
    print('AuthorizationTest success')


def GetTracksTest():
    global TestPlaylist
    all_tracks = TestPlaylist.GetAllTracks(force_refresh=True)

    assert all_tracks is not None
    # __logger.Debug('GetTracks test success')
    print('GetTracks test success')


def AddRemoveTrackTest():
    global TestPlaylist

    original_num_tracks = len(TestPlaylist.GetAllTracks())
    print(f'Playlist has {original_num_tracks} tracks.')

    try:
        TestPlaylist.AddTracks(TestTrackIds)
        new_num_tracks = len(TestPlaylist.GetAllTracks(force_refresh=True))
        assert new_num_tracks == (original_num_tracks + len(TestTrackIds))

        TestPlaylist.RemoveTracks(TestTrackIds)
        new_num_tracks = len(TestPlaylist.GetAllTracks(force_refresh=True))
        assert new_num_tracks == original_num_tracks

    except:
        print('excepting')
        TestPlaylist.RemoveTracks(TestTrackIds)
        print('Tracks removed')
        new_num_tracks = len(TestPlaylist.GetAllTracks(force_refresh=True))
        print(f'new track num: {new_num_tracks}')
        assert new_num_tracks == (original_num_tracks - len(TestTrackIds))

        TestPlaylist.AddTracks(TestTrackIds)
        new_num_tracks = len(TestPlaylist.GetAllTracks(force_refresh=True))
        assert new_num_tracks == original_num_tracks

    print(f'{len(TestTrackIds)} tracks added/removed successfully')


def GetUrlTest():
    # Todo: build test
    test_messages = ['Here\'s a link https://open.spotify.com/track/0irYSFrgXf2OH1F5NAdK6I?si=0e85a2bb98714998',
                     'https://open.spotify.com/track/0U1W2LZVUX7qTm7dDpqxh6?si=Y-NpJrguSJaotOdaFnBYbQ&utm_source=copy-link',
                     'https://open.spotify.com/track/110y35XBBoCyzv1jClu3Kv?si=BR4N0OHVRYqOV3tvzQhZQQ&context=spotify%3Aplaylist%3A1bKBY22FzGxwAsDR9CufiC']

    for message in test_messages:
        urls = Util.GetSpotifyLinks(message)
        print(f'Message: {message}\n'
              f'urls: {urls}')
        for url in urls:
            track_id = Util.GetTrackId(url)
            print(f'track id: {track_id}')
    return


def ExceptionsTest():
    global TestPlaylist
    print('Testing exceptions.')

    # Spotify link
    try:
        MLibSpotify.Links.GetSpotifyLinks('No link here.')
        raise Exception('This should have broken.')
    except:
        None

    # Track id
    try:
        MLibSpotify.Links.GetTrackId('Bad link.')
        raise Exception('This should have broken.')
    except:
        None

    # Playlist id
    try:
        MLibSpotify.Links.GetPlaylistId('Bad link')
        raise Exception('This should have broken.')
    except:
        None

    # Remove tracks
    try:
        TestPlaylist.RemoveTracks(TestTrackIds)
        TestPlaylist.RemoveTracks(TestTrackIds)
        raise Exception('This should have broken.')
    except:
        None

    # Add tracks
    try:
        TestPlaylist.AddTracks(TestTrackIds)
        TestPlaylist.AddTracks(TestTrackIds)
        raise Exception('This should have broken.')
    except:
        None

    print('All exceptions thrown')

def GetAllUserPlaylistsTest():
    all_playlists = GetAllUserPlaylists(os.getenv("REFRESH_TOKEN"))
    for playlist in all_playlists:
        None


# endregion

# region Run tests

# __logger.Info('Starting Spotify Tests')
print('Starting spotify tests')
AuthorizationTest()
GetTracksTest()
# AddRemoveTrackTest()
GetUrlTest()
ExceptionsTest()
# GetAllUserPlaylistsTest()

# endregion

# region Refresh access token

# Util.GetAuthorizationCode()
# Util.GetAccessToken()
# Util.RefreshAccessToken()

# endregion
