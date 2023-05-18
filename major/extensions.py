import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
from collections import deque
# Only for General Data like Playlistsinfo, Artistsinfo,etc.
# sp=spotipy.Spotify(
#     client_credentials_manager=SpotifyClientCredentials(
#         client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
#         client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET')
#     )
# )

# All data including user data
scope='user-library-read'
sp=spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URI'),
        scope=scope,
        requests_timeout=10
    )
)

dic={}
q = []