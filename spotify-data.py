import os  # for accessing environment variables
import time  # for execution times
import spotipy  # python library for Spotify API
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import seaborn as sns
import pandas as pd

# Retreive client_id and client_secret from environment variables
# Should be set when initializing class
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:2222/"
USERNAME = ""
SCOPE = 'user-library-read \
        playlist-read-private' 

# Setting Spotify Client Credentials
# client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Retrieving API token
token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

def get_saved_tracks(token): 
    '''
    Given user token, retrieve all users saved tracks and put into dataframe
    :param token: Spotify API token for user
    '''
    if token:
        artist_name = []
        track_name = []
        popularity = []
        track_id = []
        num_tracks = 3500 # no idea what the upper limit is
        sp = spotipy.Spotify(auth=token)
        
        for i in range(0,num_tracks,50):
            track_results = sp.current_user_saved_tracks(limit=50, offset=i)
            for item in track_results['items']:
                track = item['track']
                artist_name.append(track['artists'][0]['name'])
                track_name.aend(track['name'])
                track_id.append(track['id'])
                popularity.append(track['popularity'])
    else: # raise error
        print("Can't get token for", username)
        
    df_tracks = pd.DataFrame({'artist_name':artist_name, 
                            'track_name':track_name, 
                            'track_id':track_id, 
                            'popularity':popularity})

    df_tracks.drop_duplicates(subset=['artist_name', 'track_name'], inplace=True)

    return df_tracks


def get_track_info(tracks): 
    '''
    From list of tracks pull track info and put into dataframe

    :param tracks:  list of Spotify track URIs
    :return: dataframe of track information
    '''
    pass

def get_audio_features(self, df_tracks)
    '''
    Given a dataframe of tracks, retrives audio features for each track, 
    joins audio features, removes duplicates, and returns a dataframe 

    :param df_tracks: dataframe of track
    '''
    # Retrieve Audio Features
    rows = []
    batchsize = 100 # check batchsize in Spotify API
    None_counter = 0

    for i in range(0, len(df_tracks['track_id']), batchsize): 
        batch = df_tracks['track_id'][i:i+batchsize]
        feature_results = sp.audio_features(batch)
        
        for index, track in enumerate(feature_results):
            if track == None:
                None_counter = None_counter + 1
            else:
                rows.append(track)
                
    # print('Number of tracks where no audio features were available:', None_counter)

    df_audio_features = pd.DataFrame.from_dict(rows, orient='columns')
    df_audio_features.rename(columns = {'id': 'track_id'}, inplace=True) # rename column to match other dataframe
    self.df = pd.merge(df_tracks, df_audio_features, on='track_id', how='inner')
