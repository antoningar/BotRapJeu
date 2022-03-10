import helpers.jsonhelper as jsonhelper
import random

# récupérer une carte puriste au hasard
def get_carte_puristes():
    return jsonhelper.get_cartes_puristes()
    
# récupérer une carte mystere au hasard
def get_carte_mysteres():
    return jsonhelper.get_cartes_mystere()
    
#recuperation d'un artiste au hasard
def get_random_artists():
    artists = jsonhelper.get_artists()
    index = random.randrange(len(artists))
    return artists[index]