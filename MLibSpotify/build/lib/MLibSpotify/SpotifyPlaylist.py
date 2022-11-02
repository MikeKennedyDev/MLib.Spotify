import spotipy
from spotipy import SpotifyOAuth
# from MLibLogging import MLogger

# region Fields

# logger = MLogger.MLogger('MLibSpotify')


# endregion

class SpotifyPlaylist:

    # region Constructors

    def __init__(self, authorization_values, playlist_id):
        print(f'Modelling playlist with id: {playlist_id}')
        # logger.Info(f'Modelling playlist with id: {playlist_id}')

        auth_man = SpotifyOAuth(
            client_id=authorization_values.Client_id,
            client_secret=authorization_values.Client_secret,
            redirect_uri=authorization_values.Redirect_uri,
            scope=authorization_values.Scope)

        if 'playlist-read-collaborative' not in auth_man.scope:
            # logger.Error("Scope: 'playlist-read-collaborative' is necessary to use MLibSpotify.")
            raise PermissionError("Scope: 'playlist-read-collaborative' is necessary to use MLibSpotify.")

        self.PlaylistId = playlist_id

        self.__auth_manager = auth_man
        self.__spotify = spotipy.Spotify(auth_manager=auth_man)
        self.__allTracks = self.GetAllTracks(force_refresh=True)

    # endregion

    # region Methods

    def GetAllTracks(self, force_refresh=False):
        if not force_refresh:
            return self.__allTracks
        print(f'Populating tracks for playlist {self.PlaylistId}')
        # logger.Debug(f'Populating tracks for playlist {self.PlaylistId}')
        self.__allTracks = [item['track'] for item in
                            self.__spotify.playlist_items(playlist_id=self.PlaylistId)['items']]
        return self.__allTracks

    def AddTracks(self, tracks):
        print(f'Adding {len(tracks)} track(s) to playlist {self.PlaylistId}')
        # logger.Info(f" Adding {len(tracks)} track(s) to playlist '{self.PlaylistId}'")
        self.__spotify.playlist_add_items(playlist_id=self.PlaylistId, items=tracks)
        self.__allTracks = self.GetAllTracks(force_refresh=True)

    # endregion


class AuthorizationValues:

    def __init__(self,
                 client_id,
                 client_secret,
                 scope='playlist-read-collaborative playlist-modify-public',  # default read/write public playlists
                 redirect_uri='http://localhost:8888'):
        self.Client_id = client_id
        self.Client_secret = client_secret
        self.Redirect_uri = redirect_uri
        self.Scope = scope
