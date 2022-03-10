import random

import helpers.translateheper as translatehelper
import helpers.filehelper as filehelper

current_carte = None

cartes_puristes = list()
cartes_mysteres = list()

def init_cards():
    global cartes_puristes, cartes_mysteres    
    cartes_puristes = filehelper.get_carte_puristes()
    cartes_mysteres = filehelper.get_carte_mysteres()

# RENVOI SI IL Y A AU MOINS 2 QUESTIONS POSSIBLE DANS CHAQUE CATEGORIE
def is_available():
    global cartes_puristes, cartes_mysteres    
    return len(cartes_mysteres) > 1 and len(cartes_puristes)

# GENERE UNE CARTE MYSTERE ET L'AFFICHE        
async def choose_mystere(message):
    global cartes_mysteres
    index = random.randrange(len(cartes_mysteres))
    # recuperation de la carte
    carte = cartes_mysteres[index]
    # affichage de la carte
    await message.send(carte.label)
    await message.send(translatehelper.get_cards('mystery_point',str(carte.points)))
    #suppression de la carte dans la liste
    del cartes_mysteres[index]
    return carte.points

# GENERE UNE CARTE PURISTE ET L'AFFICHE
async def choose_puriste(message):
    global current_carte, cartes_puristes
    # recuperation de la carte
    index = random.randrange(len(cartes_puristes))
    carte = cartes_puristes[index]
    # affichage de la carte
    await message.send(carte.label)
    await message.send(translatehelper.get_cards('response'))
    #suppression de la carte dans la liste
    del cartes_puristes[index]
    current_carte = carte
    
# CATCH LA REPONSE A UNE CARTE PURISTE
async def reponse_puriste(ctx, message):
    global current_carte
    # si la carte puriste a déja etet choisit
    if current_carte is not None:
        # on fait des upper() pour eviter que la caste fasse chier
        if current_carte.answer.upper() == message.upper():
            points = current_carte.points
            await ctx.send(translatehelper.get_cards('correct_answer',current_carte.points))
            current_carte = None
            return points
        else:
            await ctx.send(translatehelper.get_cards('wrong_answer'))
