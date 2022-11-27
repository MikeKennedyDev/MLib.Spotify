import requests
from MLibSpotify import Utilities

# region Fields

__access_token = None
__client_id = None
__client_secret = None
__refresh_token = None

# endregion Fields

# region constructors

def __init__(self,
             client_id,
             client_secret,
             refresh_token,
             access_token=None,
             force_refresh=False):
    global __access_token, __refresh_token, __client_secret, __client_id

    __client_secret = client_secret
    __client_id = client_id
    __refresh_token = refresh_token

    if access_token:
        __access_token = access_token
    elif not __access_token:
        print('Creating new access token')
        # TODO: get access token

# endregion Constructors

# region Methods

def RefreshAccessToken(client_id,
                       client_secret,
                       refresh_token,
                       access_token=None,
                       force_refresh=False):
    global AccessToken

    # TODO: Validate access token works
    if not force_refresh and AccessToken:
        return AccessToken

    request_headers = {
        "Authorization": Utilities.EncodeAuthorization(client_id,
                                                       client_secret),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post("https://accounts.spotify.com/api/token",
                             headers=request_headers,
                             data=request_body)

    if not response.ok:
        raise Exception(f"Error refreshing access token: {response.json()['error']}")

    AccessToken = response.json()['access_token']
    return AccessToken

# endregion Methods