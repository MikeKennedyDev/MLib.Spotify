import GlobalSettings
import Utilities
import spotipy
from spotipy import SpotifyOAuth


class SpotifyPlaylist:

    # region Constructors

    def __init__(self, scope, playlist_id):
        print(f'Modelling playlist with id: {playlist_id}')

        auth_man = SpotifyOAuth(
            client_id=GlobalSettings.CLIENT_ID,
            client_secret=GlobalSettings.CLIENT_SECRET,
            redirect_uri=Utilities.RedirectAddress,
            scope=scope)

        if 'playlist-read-collaborative' not in auth_man.scope:
            print("you shouldn't be here")
            return
            # TODO: throw error on bad scope

        self.PlaylistId = playlist_id

        self.__auth_manager = auth_man
        self.__spotify = spotipy.Spotify(auth_manager=auth_man)
        self.__allTracks = self.GetAllTracks(force_refresh=True)

    # endregion

    # region Methods

    def GetAllTracks(self, force_refresh=False):
        if not force_refresh:
            return self.__allTracks
        self.__allTracks = [item['track'] for item in
                            self.__spotify.playlist_items(playlist_id=self.PlaylistId)['items']]
        return self.__allTracks

    def AddTrack(self, tracks):
        print('Adding tracks:')
        for track in tracks:
            print(track)
        self.__spotify.playlist_add_items(self.PlaylistId, tracks)

    # endregion
