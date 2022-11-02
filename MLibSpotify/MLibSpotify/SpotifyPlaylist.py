import requests

# region Fields

# logger = MLogger.MLogger('MLibSpotify')

__client_id = 'bf7bb8ab99894704bed9dfadf4535ef2'
__client_secret = '44cb0a59f67b4a3dbfdf0ac7c8f4c57a'
base_spotify_api = 'https://api.spotify.com/v1/'


# endregion

# region Static methods
def GetPlaylistTracksApi(playlist_id):
    return f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'


# endregion

class SpotifyPlaylist:
    # region Fields

    PlaylistId = None
    __redirect_uri = 'http://localhost:8888/callback'
    __scope = 'playlist-read-collaborative playlist-modify-public'
    __auth_token = None
    __all_tracks = []

    # endregion

    # region Constructors

    def __init__(self, auth_token, playlist_id, scope=None, redirect_uri=None):

        self.PlaylistId = playlist_id

        if redirect_uri is not None:
            self.__redirect_uri = redirect_uri

        if auth_token is not None:
            self.__auth_token = auth_token

        if scope is not None:
            self.__scope = scope

    # endregion

    # region Methods

    def GetAllTracks(self, force_refresh=False):

        if not force_refresh and self.__allTracks:
            return self.__allTracks

        print(f'Populating tracks for playlist {self.PlaylistId}')

        endpoint = GetPlaylistTracksApi(self.PlaylistId)
        headers = {"Authorization": f"Bearer {self.__auth_token}"}
        print(f'Targeting endpoint: {endpoint}')
        print(f'Using auth values: {headers}')
        response = requests.get(endpoint, headers=headers)

        print(response)

        return None

    def AddTracks(self, tracks):
        print(f'Adding {len(tracks)} track(s) to playlist {self.PlaylistId}')
        # logger.Info(f" Adding {len(tracks)} track(s) to playlist '{self.PlaylistId}'")
        self.__spotify.playlist_add_items(playlist_id=self.PlaylistId, items=tracks)
        self.__allTracks = self.GetAllTracks(force_refresh=True)

    # endregion


class AuthorizationValues:

    def __init__(self, auth_token):
        self.authorization_token = auth_token
