import requests

from MLibSpotify import Utilities, Links, Authorization

# region Fields

base_spotify_api = 'https://api.spotify.com/v1/'
__refresh_token = None
__access_token = None
__client_id = None
__client_secret = None

# endregion


class SpotifyPlaylist:
    # region Fields

    PlaylistId = None
    PlaylistName = None
    __all_tracks = []

    # endregion

    # region Constructors

    def __init__(self,
                 playlist_id,
                 client_id,
                 client_secret,
                 refresh_token):

        global __refresh_token, __client_id, __client_secret, __access_token

        # Initialize playlist values
        self.PlaylistId = playlist_id
        __refresh_token = refresh_token
        __client_id = client_id
        __client_secret = client_secret

        # Populate playlist data
        self.PlaylistName = self.GetPlaylistName()
        self.PlaylistUrl = Links.GetSpotifyPlaylistUrl(self.PlaylistId)
        self.__refresh_access_token()
        __access_token = Authorization.RefreshAccessToken(__client_id, __client_secret, __refresh_token)
        self.__all_tracks = self.GetAllTracks(force_refresh=True)

        print(f'Playlist object created for playlist {playlist_id} and populated with {len(self.__all_tracks)} tracks.')

    # endregion

    # region Methods

    def GetPlaylistName(self):
        endpoint = Utilities.GetPlaylistEndpoint(self.PlaylistId)
        headers = {"Authorization": f"Bearer {self.__access_token}"}
        response = requests.get(endpoint, headers=headers)

        if not response.ok:
            self.__handle_error(response)
            return self.GetPlaylistName()

        return response.json()["name"]

    def GetAllTracks(self, force_refresh=False):
        global __access_token

        if not force_refresh and self.__all_tracks:
            return self.__all_tracks

        endpoint = Utilities.GetPlaylistTracksEndpoint(self.PlaylistId)
        headers = {"Authorization": f"Bearer {__access_token}"}
        response = requests.get(endpoint, headers=headers)

        # Error handling
        if not response.ok:
            self.__handle_error(response)
            self.GetAllTracks(force_refresh=True)
            return

        self.__all_tracks = [item['track'] for item in response.json()['items']]
        return self.__all_tracks

    def AddTracks(self, track_ids):

        # Refresh tracks before add
        self.__all_tracks = self.GetAllTracks(force_refresh=True)

        playlist_track_ids = [track['id'] for track in self.__all_tracks]
        tracks_to_add = list(set(track_ids) - set(playlist_track_ids))

        if len(tracks_to_add) == 0:
            raise Exception('Specified tracks already in playlist.')

        print(f'Adding {len(tracks_to_add)} track(s) to playlist {self.PlaylistId}')

        headers = {"Authorization": f"Bearer {self.__access_token}"}
        playlist_chunks = Utilities.chunker(tracks_to_add, 10)

        for chunk in playlist_chunks:
            endpoint = Utilities.GetAddTracksEndpoint(self.PlaylistId, tracks=chunk)
            response = requests.post(endpoint, headers=headers)
            if not response.ok:
                self.__handle_error(response)
                self.AddTracks(track_ids=track_ids)
                return




        # Update internal track list
        self.__all_tracks = self.GetAllTracks(force_refresh=True)

    def RemoveTracks(self, track_ids):

        # Refresh tracks
        self.__all_tracks = self.GetAllTracks(force_refresh=True)

        playlist_track_ids = [track['id'] for track in self.__all_tracks]
        tracks_to_remove = [value for value in track_ids if value in playlist_track_ids]
        if len(tracks_to_remove) == 0:
            raise Exception('Tracks not found in playlist.')

        print(f'Removing {len(tracks_to_remove)} track(s) from playlist {self.PlaylistId}')

        playlist_chunks = Utilities.chunker(tracks_to_remove, 10)
        endpoint = Utilities.GetRemoveTracksEndpoint(self.PlaylistId)
        headers = {"Authorization": f"Bearer {self.__access_token}"}

        for chunk in playlist_chunks:
            track_uris = [{"uri": f"spotify:track:{track_id}"} for track_id in playlist_chunks]

            # I don't know why, but spotify complains unless this format is used here
            body = str({"tracks": track_uris}).replace("'", '\"')

            response = requests.delete(endpoint, headers=headers, data=body)
            if not response.ok:
                self.__handle_error(response)
                self.AddTracks(track_ids=track_ids)
                return

        # Update internal track list
        self.__all_tracks = self.GetAllTracks(force_refresh=True)

    def __handle_error(self, response):
        error_message = response.json()['error']['message']

        # Refresh access token if expired
        if 'access token expired' in error_message \
                or 'Invalid access token' in error_message:
            self.__refresh_access_token()
            return

        # Throw exception otherwise
        raise Exception(f'Error returned from Spotify API call: {error_message}')

    def __refresh_access_token(self):

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

def GetAllUserPlaylists(access_token):
    endpoint = Utilities.GetAllPlaylistsEndpoint()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(endpoint, headers=headers)

    print('checkin')
    return
