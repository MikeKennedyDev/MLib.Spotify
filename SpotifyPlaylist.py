import Utilities
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from SpotifyTrack import SpotifyTrack


class SpotifyPlaylist:

    # region Constructors

    def __init__(self, auth_manager, playlist_id):
        print(f'Creating playlist with id: {playlist_id}')
        if 'playlist-read-collaborative' not in auth_manager.scope:
            print("you shouldn't be here")
            # TODO: throw error on bad scope

        self.PlaylistId = playlist_id

        self.__auth_manager = auth_manager
        self.__spotify = spotipy.Spotify(auth_manager=auth_manager)
        self.__allTracks = self.GetAllTracks(force_refresh=True)

    # endregion

    # region Methods

    def GetAllTracks(self, force_refresh=False):
        if not force_refresh:
            return self.__allTracks
        self.__allTracks = [item['track'] for item in
                            self.__spotify.playlist_items(playlist_id=self.PlaylistId)['items']]
        return self.__allTracks

    def AddTrack(self, track_id):

        return
        # if trackId in [self.__allTracks['id']]:

    # endregion
