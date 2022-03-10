import requests

import settings
import helpers.loggerhelper as loggerhelper

URL_SEARCH = "https://api.genius.com/"
HEADERS = {'Authorization': 'Bearer ' + settings.TOKEN_GENIUS}
# Les freestyles sont blacklistés, choix perso mais possibilité d'enlever ça
BLACK_LIST = ['FREESTYLE','Translation', 'Traduzione', 'grunt']

# Verifie que tous les artists sont dans le titre du son
def is_artists_in_title(artist_1, artist_2, full_title):
    # ici on fait des trucs qui servent à rien
    # si il y a un espace dans le nom de l'artise (ex: "alpha wann")
    # le if "alpha wann" in "alpha wann - le piege" va retourne False
    # je comprend pas pourquoi mais bon du coup je coupe "alpha wann" en ["alpha", "wann"]
    # et je verifie que "alpha" et "wann" sont bien dans le titre
    word = list()
    # decoupage des noms d'artistes
    [word.append(x) for x in artist_1.split(' ')]
    [word.append(y) for y in artist_2.split(' ')]
    # on verifie que tous les mots decoupés sont dans le titre
    for w in word:
        if w not in full_title:
            return False
    return True

# Vérifie que les artistes sont bien dans le titre du son
def search(artist_1, artist_2):
    url = "%ssearch?q=%s %s" % (URL_SEARCH, artist_1, artist_2)
    # requete rap genius 
    r = requests.get(url, headers=HEADERS)
    loggerhelper.log_request(url, 'RAPGENIUS', 'genius search')
    r = r.json()
    # parcours de toutes les chansons
    for hit in r['response']['hits']:
        full_title = hit['result']['full_title'].upper().replace('’', '\'')
        # verification que le titre n'a pas des mots blacklisté
        if any(x.upper() in full_title for x in BLACK_LIST):
            continue
        # verification que le son est bien un feat des deux artistes
        if is_artists_in_title(artist_1.upper(), artist_2.upper(), full_title):
            return hit['result']['title']

    return None
