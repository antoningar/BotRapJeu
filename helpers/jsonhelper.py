import json
from modeles import Carte_puriste, Carte_mystere

def get_cartes_puristes():
    liste_cartes = list()
    with open('assets/cartes_puriste.json','r', encoding="utf-8") as f:
        json_file = json.load(f)
        cartes = json_file['cartes_puriste']
        for carte in cartes:
            liste_cartes.append(Carte_puriste(carte['label'], carte['answer'], carte['points']))
        
        return liste_cartes
        
def get_cartes_mystere():
    liste_cartes = list()
    with open('assets/cartes_mystere.json','r', encoding="utf-8") as f:
        json_file = json.load(f)
        cartes = json_file['cartes_mystere']
        for carte in cartes:
            liste_cartes.append(Carte_mystere(carte['label'], carte['points']))
        
        return liste_cartes

def get_artists():
    with open('assets/artists.json', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        return json_file['artists']

def get_token_spotify():
    with open('assets/spotify.json', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        return json_file['token_spotify']

def set_token_spotify(token):
    with open('assets/spotify.json', 'w', encoding='utf-8') as f:
        json.dump({'token_spotify':token},f)