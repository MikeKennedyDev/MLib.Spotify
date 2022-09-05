import Utilities
import requests


class SpotifyPlaylist:

    # region Constructors

    def __init__(self, playlist_id, auth_token):
        self.__track_api_address = None
        self.__playlist_id = playlist_id
        self.__playlist_api_address = Utilities.GetPlaylistUri(playlist_id)
        self.__headers = {'Authorization': f'Bearer {auth_token}'}
        self.__playlist = requests.get(self.__playlist_api_address, headers=self.__headers).json()
        # TODO: Throw here if there's not playlist

        self.Tracks = self.__playlist['tracks']['items']
        self.Playlist_id = playlist_id
        self.Name = self.__playlist['name']

    # endregion

    # region Methods

    def AddTrack(self, track_id):
        print(f'adding {track_id} to {self.__playlist_id}')
        self.__track_api_address = Utilities.PostTrackUri(self.__playlist_id)
        headers = {'spotify:track': track_id}
        response = requests.post(self.__track_api_address, headers=headers)
        print(response)

    # endregion
