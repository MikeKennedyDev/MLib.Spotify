import Utilities
import requests


class SpotifyTrack:

    # region Constructors

    def __init__(self, track_id, auth_token):
        self.__track_api_address = Utilities.GetTrackUri(track_id)
        self.__headers = {'Authorization': f'Bearer {auth_token}'}
        self.__track = requests.get(self.__track_api_address, headers=self.__headers).json()
        # TODO: Throw here if there's not track exists

        self.TrackId = track_id
        self.Name = self.__track['name']
        self.TrackUri = self.__track['uri']

    # endregion

    # region Methods



    # endregion
