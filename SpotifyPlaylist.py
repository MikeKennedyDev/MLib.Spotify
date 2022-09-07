import Utilities
import requests

from SpotifyTrack import SpotifyTrack


class SpotifyPlaylist:

    # region Constructors

    def __init__(self, playlist_id, auth_token):
        self.__track_api_address = None
        self.__playlist_id = playlist_id
        self.__playlist_api_address = Utilities.GetPlaylistUri(playlist_id)
        self.__headers = {'Authorization': f'Bearer {auth_token}'}
        self.__playlist = requests.get(self.__playlist_api_address, headers=self.__headers).json()
        # TODO: Throw here if there's not playlist

        self.PlaylistId = playlist_id
        self.Name = self.__playlist['name']
        self.Tracks = self.__getAllTracks(self.__playlist['tracks']['items'])

    # endregion

    # region Methods

    def __getAllTracks(self, raw_tracks):
        print('Populating tracks...')
        allTracks = []
        for track in raw_tracks:
            allTracks.append(SpotifyTrack(track['track']['id'], self.__headers))
        print(f'Playlist object "{self.Name}" populated with {len(allTracks)} tracks')
        return allTracks

    def AddTrack(self, spotifyTrack):
        print(f'adding "{spotifyTrack.Name}" to playlist "{self.Name}"')
        self.__track_api_address = Utilities.PostTrackUri(self.__playlist_id)
        headers = {'spotify:track': spotifyTrack.Track_id}
        response = requests.post(self.__track_api_address, headers=headers)
        # TODO: Add error handling for failure
        print(response)

    # endregion
