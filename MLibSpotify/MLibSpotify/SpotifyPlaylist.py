import requests
from MLibSpotify import Utilities

# region Fields

__client_id = 'bf7bb8ab99894704bed9dfadf4535ef2'
__client_secret = '44cb0a59f67b4a3dbfdf0ac7c8f4c57a'
base_spotify_api = 'https://api.spotify.com/v1/'


# endregion


class SpotifyPlaylist:
    # region Fields

    PlaylistId = None
    __all_tracks = []
    __refresh_token = None
    __access_token = None
    __client_id = None
    __client_secret = None

    # endregion

    # region Constructors

    def __init__(self,
                 playlist_id,
                 client_id,
                 client_secret,
                 refresh_token):

        # Initialize playlist values
        self.PlaylistId = playlist_id
        self.__refresh_token = refresh_token
        self.__client_id = client_id
        self.__client_secret = client_secret

        # Populate playlist tracks
        self.__refresh_access_token()
        self.__all_tracks = self.GetAllTracks(force_refresh=True)

        print(f'Playlist object created for playlist {playlist_id} and populated with {len(self.__all_tracks)} tracks.')

    # endregion

    # region Methods

    def GetAllTracks(self, force_refresh=False):

        if not force_refresh and self.__all_tracks:
            return self.__all_tracks

        endpoint = Utilities.GetPlaylistEndpoint(self.PlaylistId)
        headers = {"Authorization": f"Bearer {self.__access_token}"}
        response = requests.get(endpoint, headers=headers)

        # Error handling
        if not response.ok:
            self.__handle_error(response)

        return [item['track'] for item in response.json()['items']]

    def AddTracks(self, track_ids):
        print(f'Adding {len(track_ids)} track(s) to playlist {self.PlaylistId}')

        endpoint = Utilities.GetAddTracksEndpoint(self.PlaylistId, tracks=track_ids)
        headers = {"Authorization": f"Bearer {self.__access_token}"}

        response = requests.post(endpoint, headers=headers)
        if not response.ok:
            self.__handle_error()

        # Update internal track list
        self.__all_tracks = self.GetAllTracks(force_refresh=True)

    def __handle_error(self, response):
        error_message = response.json()['error']['message']

        # Refresh access token if expired
        if 'access token expired' in error_message \
                or 'Invalid access token' in error_message:
            self.__refresh_access_token()
            self.GetAllTracks(force_refresh=True)
            return

        # Throw exception otherwise
        raise Exception(f'Error returned from Spotify API call: {error_message}')
        return

    def __refresh_access_token(self):
        print('Refreshing access_token')

        request_headers = {
            "Authorization": Utilities.EncodeAuthorization(self.__client_id,
                                                           self.__client_secret),
            "Content-Type": "application/x-www-form-urlencoded"
        }

        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": self.__refresh_token
        }

        response = requests.post("https://accounts.spotify.com/api/token",
                                 headers=request_headers,
                                 data=request_body)

        if not response.ok:
            raise Exception(f"Error refreshing access token: {response.json()['error']}")

        self.__access_token = response.json()['access_token']

    # endregion
