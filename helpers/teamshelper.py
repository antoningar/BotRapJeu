import settings

import helpers.translateheper as translatehelper
import helpers.loggerhelper as loggerhelper
from modeles import Team

team_msg = None

teams = (Team('Bleu'), Team('Rouge'))

# ----------------------------------------------------------
# ----------------------------------------------------------
# FONCTIONS UTILITAIRE POUR LA GESTIOND ES EQUIPES
# ----------------------------------------------------------
# ----------------------------------------------------------

# reset teams
def reset_teams():
    global teams
    teams = (Team('Bleu'), Team('Rouge'))

# Recupere la team en fonctions de la couleur voulut
def get_team_by_name(name):
    global teams
    return [team for team in teams if team.name == name][0]

# Recupere la current team
def get_current_team():
    global teams
    return [team for team in teams if team.current][0]

    
# Recupere la team adverse a la current
def get_other_team():
    global teams
    return [team for team in teams if not team.current][0]

# retourne si le joueur est dans la team actuelle
def is_player_in_current_team(player):
    global teams
    current_team = get_current_team()
    return current_team.is_player_in_team(player)

# chositi la team courant en fonction du joueur
# Attention : n'update pas l'autre team 
def set_current_team(player):
    global teams
    blue_team = get_team_by_name('Bleu')
    red_team = get_team_by_name('Rouge')
    if any(player in p for p in blue_team.players):
        blue_team.current = True
        return 'Bleu'
    if any(player in p for p in red_team.players):
        red_team.current = True
        return 'Rouge'

# swap la current team
def swap_current_team():
    global teams
    for t in teams:
        t.current = True if not t.current else False
    return get_current_team()

# Mets toutes les teams a current = False
def reset_current_team():
    global teams
    for t in teams:
        t.current = False

# Incremente le score de l'equipe n'étant pas la current team
def update_score_other_team():
    get_other_team().score += settings.POINTS_VICTOIRE

# Incremente le score de la current team
def update_score_current_team(points=1):
    get_current_team().score += points

# Ajoute le malus de point à l'équipe
def add_malus():
    get_current_team().score -= 1

# ----------------------------------------------------------
# ----------------------------------------------------------
# GESTION DE LA CREATION DES EQUIPES AVEC LES EMOJIS
# ----------------------------------------------------------
# ----------------------------------------------------------

#Fonction qui afffiche le menu de choix des equipes
async def welcome(bot):
    global team_msg
    channel = bot.get_channel(settings.CHANNEL_ID)
    message_bot = await channel.send(translatehelper.get_guidelines('welcome'))
    team_msg = message_bot
    # ajout des emojis
    await message_bot.add_reaction("\U0001F534")
    await message_bot.add_reaction("\U0001F535")

# Ajout d'une emote == Join d'une equipe
async def on_raw_reaction_add(payload):
    global team_msg, teams
    if team_msg is not None and payload.message_id == team_msg.id:    
        print(f"""Selectionne : {team_msg.id}""")
        if payload.emoji.name == '\U0001F534':
            # PERMET DETRE DANS LES DEUX TEAMS
            # A DELETE & DECOMMENTER HORS TESTS
            if True:
            #if str(payload.member) not in red_team:
                loggerhelper.log_reaction_added(team_msg.id, payload.member)
                player_red=str(payload.member).split('#')[0]
                red_team = get_team_by_name('Rouge')
                red_team.players.append(player_red)
                
        if payload.emoji.name == '\U0001F535':
            # PERMET DETRE DANS LES DEUX TEAMS
            # A DELETE & DECOMMENTER HORS TESTS
            if True:
            # if str(payload.member) not in blue_team:
                loggerhelper.log_reaction_added(team_msg.id, payload.member)
                player_blue=str(payload.member).split('#')[0]
                blue_team = get_team_by_name('Bleu')
                blue_team.players.append(player_blue)

# Suppression d'une emote == Leave d'une equipe
async def on_raw_reaction_remove(self, payload):
    global team_msg, teams
    if team_msg is not None and payload.message_id == team_msg.id:
        # On va cherche le nom du joueur via l'id
        user_name = await self.fetch_user(payload.user_id)
        red_team = get_team_by_name('Rouge')
        blue_team = get_team_by_name('Bleu')
        loggerhelper.log_reaction_delete(team_msg.id, payload.user)
        if payload.emoji.name == '\U0001F534' and red_team is not None:
            player_red=str(user_name).split('#')[0]
            red_team.players.remove(player_red)

        if payload.emoji.name == '\U0001F535' and blue_team is not None:
            player_blue=str(user_name).split('#')[0]
            blue_team.players.remove(player_blue)