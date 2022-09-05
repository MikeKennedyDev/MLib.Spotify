import GlobalSettings
import requests

def __GetAccessToken():
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': GlobalSettings.CLIENT_ID,
        'client_secret': GlobalSettings.CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    return auth_response_data['access_token']

AUTH_URL = 'https://accounts.spotify.com/api/token'
AuthToken = __GetAccessToken()
headers = {'Authorization': f'Bearer {AuthToken}'}


# api_url = f'https://api.spotify.com/v1/playlists/{GlobalSettings.SHARED_PLAYLIST_ID}'
#
# # track id: spotify:track:6y0igZArWVi6Iz0rj35c1Y
# response = requests.get(api_url, headers=headers).json()
# playlist_name = response['name']
# playlist_owner = response['owner']['display_name']
# print(f'Playlist: {playlist_name}')
# print(f'Owner: {playlist_owner}')

def AddTrack(playlist_id, track_id):
    print(f'Adding track {track_id} to playlist {playlist_id}')


def GetAllTracks(api_endpoint):
    response = requests.get(api_endpoint, headers=headers).json()
    return response['tracks']['items']
