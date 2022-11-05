import os

import requests

# region Fields

# logger = MLogger.MLogger('MLibSpotify')

__client_id = 'bf7bb8ab99894704bed9dfadf4535ef2'
__client_secret = '44cb0a59f67b4a3dbfdf0ac7c8f4c57a'
base_spotify_api = 'https://api.spotify.com/v1/'


# endregion

# region Static methods
def GetPlaylistEndpoint(playlist_id):
    return f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'


def GetAddTracksEndpoint(playlist_id, tracks):
    endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris='
    uris = '%2C'.join([f'spotify%3Atrack%3A{track}' for track in tracks])
    return f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={uris}'


# endregion

class SpotifyPlaylist:
    # region Fields

    PlaylistId = None
    __all_tracks = []

    # endregion

    # region Constructors

    def __init__(self, playlist_id):
        self.PlaylistId = playlist_id
        self.__allTracks = self.GetAllTracks(force_refresh=True)
        print(f'Playlist object created for playlist {playlist_id} and populated with {len(self.__allTracks)} tracks.')

    # endregion

    # region Methods

    def GetAllTracks(self, force_refresh=False):

        if not force_refresh and self.__allTracks:
            return self.__allTracks

        endpoint = GetPlaylistEndpoint(self.PlaylistId)
        headers = {"Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"}
        response = requests.get(endpoint, headers=headers)

        if not response.ok:
            raise Exception('Error returned from Spotify API call')

        return [item['track'] for item in response.json()['items']]

    def AddTracks(self, track_ids):
        print(f'Adding {len(track_ids)} track(s) to playlist {self.PlaylistId}')

        # logger.Info(f" Adding {len(tracks)} track(s) to playlist '{self.PlaylistId}'")

        endpoint = GetAddTracksEndpoint(self.PlaylistId, tracks=track_ids)
        headers = {"Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"}

        response = requests.post(endpoint, headers=headers)
        if not response.ok:
            raise Exception(f'Error returned from Spotify Post API: {response.json()["error"]}')

        # Show new tracks in __allTracks
        self.__allTracks = self.GetAllTracks(force_refresh=True)

    # endregion
