def GETPlaylistUri(playlist_id):
    return f'https://api.spotify.com/v1/playlists/{playlist_id}'


def GETTrackUri(track_id):
    return f'https://api.spotify.com/v1/tracks/{track_id}'


def POSTTrackUri(playlist_id, track_uri):
    formatted_uri = track_uri.replace(':', '%3A')
    return f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={formatted_uri}"


def POSTCreatePlaylist(user_id, playlist_name, playlist_description):
    body = {'name': playlist_name,
            'description': playlist_description,
            'public': True}

    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    return url, body


# NOTE: This value must match the redirect
# URI on the Spotify Developer Dashboard
RedirectAddress = 'http://localhost:8888'

# def GetAuthToken(scope):
#     auth_url = 'https://accounts.spotify.com/api/token'
#     auth_response = requests.post(auth_url, {
#         'grant_type': 'client_credentials',
#         'client_id': GlobalSettings.CLIENT_ID,
#         'client_secret': GlobalSettings.CLIENT_SECRET,
#         'scope': scope
#     }).json()
#
#     return auth_response['access_token']
