from MLibSpotify.MLibSpotify.SpotifyPlaylist import SpotifyPlaylist
from MLibSpotify.MLibSpotify.SpotifyPlaylist import AuthorizationValues
import GlobalSettings

# region Fields

TestPlaylistId = '2UmDYQxgIDaKikeG53Ffd5'
TestTrackIds = ['56rgqDNRIqKq0qIMdu7r4r', '1rWzYSHyZ5BiI4DnDRCwy7']


# endregion

# region Test Methods

def AuthorizationTest():
    auth = AuthorizationValues(client_id=GlobalSettings.CLIENT_ID,
                               client_secret=GlobalSettings.CLIENT_SECRET,
                               scope='playlist-read-collaborative')

    test_playlist = SpotifyPlaylist(authorization_values=auth, playlist_id=TestPlaylistId)
    assert test_playlist is not None


def GetTracksTest():
    auth = AuthorizationValues(client_id=GlobalSettings.CLIENT_ID,
                               client_secret=GlobalSettings.CLIENT_SECRET,
                               scope='playlist-read-collaborative')
    playlist = SpotifyPlaylist(auth, playlist_id=TestPlaylistId)
    all_tracks = playlist.GetAllTracks(force_refresh=True)
    assert all_tracks is not None


def TrackAddTest():
    auth = AuthorizationValues(client_id=GlobalSettings.CLIENT_ID,
                               client_secret=GlobalSettings.CLIENT_SECRET,
                               scope='playlist-read-collaborative playlist-modify-public')
    playlist = SpotifyPlaylist(auth, playlist_id=TestPlaylistId)

    original_num_tracks = len(playlist.GetAllTracks())
    print(f'Originally {original_num_tracks} tracks')

    playlist.AddTracks(TestTrackIds)
    print(f'{len(TestTrackIds)} tracks added')

    new_num_tracks = len(playlist.GetAllTracks(force_refresh=True))
    print(f'Now {new_num_tracks} tracks')

    assert new_num_tracks == (original_num_tracks + len(TestTrackIds))


# endregion

# region Run tests

AuthorizationTest()
GetTracksTest()
TrackAddTest()

# endregion
