import spotipy
from spotipy import SpotifyClientCredentials

import settings
import helpers.jsonhelper as jsonhelper
import helpers.seleniumhelper as seleniumhelper
import helpers.loggerhelper as loggerhelper

import requests
import re

SPOTIFY_URL = 'https://api.spotify.com/v1/search'

def match(item, artist):
    for spotify_artist in item['artists']:
        spotify_artist = spotify_artist['name'].upper()
        if artist.upper() == spotify_artist:
            return True
    return False

async def verify(ctx, artist_1, artist_2):
    artists = list()
    artists.append(artist_1)
    artists.append(artist_2)
    spotify_headers = {
        "Authorization": "Bearer " + jsonhelper.get_token_spotify()
    }
    url = '%s?q=%s %s&type=track' % (SPOTIFY_URL, artist_1, artist_2)
    r = requests.get(url, headers=spotify_headers)
    loggerhelper.log_request(url, 'SPOTIFY', 'spotify search')
    r_json = r.json()
    if 'error' in r_json:
        print('TOKEN EXPIRED')
        token = None
        while token is None:
            print(token)
            await ctx.send('La régie a besoin d\'un peu de temps pour vérifier, ça arrive dans moins d\'une minute !')
            token = get_token()
        print('NEW TOKEN %s' % token)
        jsonhelper.set_token_spotify(token)
        return await verify(ctx, artist_1, artist_2)
    for item in r_json['tracks']['items']:
        if item['type'] == 'track':
            if match(item, artist_1) and match(item, artist_2):
                # On enleve ce qui est en pârenthese
                # car souvent cest les autres artists en feat
                # ça donne des indices pour le prochain feat
                regex = "[\(\[].*?[\)\]]"
                title = re.sub(regex, "", item['name'])
                return title

def get_token():
    spotify_cred_manager = SpotifyClientCredentials(client_id=settings.ID_SPOTIFY, client_secret=settings.SECRET_SPOTIFY)
    token = spotify_cred_manager.get_access_token()
    return token['access_token']

get_token()