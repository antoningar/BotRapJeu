
from discord.ext import commands

import settings
import helpers.carteshelper as carteshelper
import helpers.rolandgamoshelper as rolandhelper
import helpers.teamshelper as teamshelper
import helpers.vocalhelper as vocalhelper
import helpers.translateheper as translatehelper
import helpers.loggerhelper as loggerhelper
import helpers.leaderboardhelper as leaderboardhelper

START_COMMAND = 'okletsgo'
MUTE_COMMAND = 'mute'
UNMUTE_COMMAND = 'unmute'
RED_TEAM_COMMAND = 'red_team_list'
BLUE_TEAM_COMMAND = 'blue_team_list'
HELP_COMMAND = 'aide'
ROLAND_COMMAND = 'roland'
REROLL_COMMAND = 'reroll'
BUZZ_COMMAND = 'buzz'
ROLAND_RESPONSE_COMMAND = 'a'
FF_COMMAND = 'f'
LEAD_COMMAND = 'lead'
LEADERBOARD_COMMAND = 'leaderboard'
CARDS_COMMAND = 'cartes'
CARD_MYSTERE_COMMAND = 'mystere'
CARD_PURIST_COMMAND = 'puriste'
CARD_RESPONSE = 'r'

state = None
bot = commands.Bot(command_prefix='$')


# ----------------------------------------------------------
# ----------------------------------------------------------
# FUNCTIONS GLOBALS
# ----------------------------------------------------------
# ----------------------------------------------------------

def is_message_valid(message):
    return message.author != bot.user and message.channel.name == settings.CHANNEL_NAME

# reset toutes les variables globales
def reset():
    global state
    state = None
    teamshelper.reset_teams()

# permet de mute le bot
@bot.command(name=MUTE_COMMAND)
async def start_command(ctx):
    loggerhelper.log_command(MUTE_COMMAND, ctx.author)
    vocalhelper.set_is_muted(True)

# permet de unmute le bot
@bot.command(name=UNMUTE_COMMAND)
async def start_command(ctx):
    loggerhelper.log_command(UNMUTE_COMMAND, ctx.author)
    vocalhelper.set_is_muted(False)

# ----------------------------------------------------------
# ----------------------------------------------------------
# FONCTION EXECUTE AU LANDEMENT DU BOT (LANCEMENT DU SCRIPT)
# ----------------------------------------------------------
# ----------------------------------------------------------

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    channel = await bot.fetch_channel(settings.CHANNEL_ID)
    print(dir(channel))# Sert à lister les fonctionnalités de la variable "channel"
    carteshelper.init_cards()

# ----------------------------------------------------------
# ----------------------------------------------------------
# LIS LES MESSAGES ET LANCE LES JEUX
# ----------------------------------------------------------
# ----------------------------------------------------------

# ----------------------------------------------------------
# GESTION DES EQUIPES
# ----------------------------------------------------------

# Lancement du bot avec le choix des equipes
@bot.command(name=START_COMMAND)
async def start_command(ctx):
    global state
    if not is_message_valid(ctx):
        return
    loggerhelper.log_command(START_COMMAND, ctx.author)
    await teamshelper.welcome(bot)
    await ctx.send(translatehelper.get_roland('how_to_start_roland'))
    reset()
    state = "TEAMS"

# Liste l'équipe rouge
@bot.command(name=RED_TEAM_COMMAND)
async def list_red_team_command(ctx):
    if not is_message_valid(ctx):
        return
    loggerhelper.log_command(RED_TEAM_COMMAND, ctx.author)
    await ctx.send(str(teamshelper.get_team_by_name('Rouge')))

# Liste l'équipe bleu
@bot.command(name=BLUE_TEAM_COMMAND)
async def list_blue_team_command(ctx):
    if not is_message_valid(ctx):
        return
    loggerhelper.log_command(BLUE_TEAM_COMMAND, ctx.author)
    await ctx.send(str(teamshelper.get_team_by_name('Bleu')))

# ----------------------------------------------------------
# RECUPERATION DES AJOUTS D'EMOJI
# ----------------------------------------------------------

# Recupere l'ajout d'une emote et ajoute dans l'equipe
@bot.event
async def on_raw_reaction_add(payload):
    global state
    if state == 'TEAMS':
        await teamshelper.on_raw_reaction_add(payload)

# Recupere la suppression d'une emote et supprime le joueur de l'equipe
@bot.event
async def on_raw_reaction_remove(payload):
    global state
    if state == 'TEAMS':
        await teamshelper.on_raw_reaction_remove(bot, payload)

# ----------------------------------------------------------
# ----------------------------------------------------------
# ROLAND GAMOS
# ----------------------------------------------------------
# ----------------------------------------------------------

#command help
@bot.command(name=HELP_COMMAND)
async def help_command(ctx):
    loggerhelper.log_command(HELP_COMMAND, ctx.author)
    await ctx.message.delete()
    await ctx.send(translatehelper.get_guidelines('help'))
    await list_red_team_command(ctx)
    await list_blue_team_command(ctx)

# Lance le  roland gamos
# Choisi le premier artists
@bot.command(name=ROLAND_COMMAND)
async def roland_command(ctx):
    global state
    if not is_message_valid(ctx) or state is None:
        return
    loggerhelper.log_command(ROLAND_COMMAND, ctx.author)
    teamshelper.reset_current_team()
    await ctx.send(translatehelper.get_roland('started_roland'))
    await rolandhelper.get_first_artist(ctx)
    await ctx.send(translatehelper.get_roland('how_to_buzz'))
    state = "ROLAND_BEGINING"

# Permet de reroll si personne en connait le rappeur
@bot.command(name=REROLL_COMMAND)
async def reroll_first_artist(ctx):
    global state
    if not is_message_valid(ctx):
        return
    loggerhelper.log_command(REROLL_COMMAND, ctx.author)
    player = ctx.author.name
    if state == 'ROLAND' and teamshelper.is_player_in_current_team(player):
        await rolandhelper.get_first_artist(ctx)

# Buzzer pour prendre la main
@bot.command(name=BUZZ_COMMAND)
async def buzz_roland(ctx):
    global state
    if is_message_valid(ctx) and state == 'ROLAND_BEGINING':
        loggerhelper.log_command(BUZZ_COMMAND, ctx.author)
        state = 'ROLAND'
        player = ctx.author.name
        current_team_name = teamshelper.set_current_team(player)
        if current_team_name is not None:
            await ctx.send(translatehelper.get_team('team_lead',current_team_name))
            await ctx.send(translatehelper.get_roland('how_to_next_feat'))

# Catch du deuxieme artiste
@bot.command(name=ROLAND_RESPONSE_COMMAND)
async def second_artist(ctx, *args):
    global state
    if not is_message_valid(ctx):
        return
    player = ctx.author
    loggerhelper.log_command(ROLAND_RESPONSE_COMMAND, player)
    if state == 'ROLAND' and teamshelper.is_player_in_current_team(player.name):
        r = await rolandhelper.get_second_artist(ctx, ' '.join(args))
        if r == 1:
            await vocalhelper.play_win(bot, player.id)
            current_team = teamshelper.swap_current_team()
            await ctx.send(translatehelper.get_team('team_lead', current_team.name))
        else:
            teamshelper.add_malus()
            current_team = teamshelper.get_current_team()
            leaderboardhelper.update_users(current_team.players, -1)
            await vocalhelper.play_loose(bot, player.id)

# Abandon de la game
@bot.command(name=FF_COMMAND)
async def abandon(ctx):
    global state, bot
    if not is_message_valid(ctx):
        return
    player = ctx.author
    loggerhelper.log_command(FF_COMMAND, player)
    if state == 'ROLAND' and teamshelper.is_player_in_current_team(player.name):
        await vocalhelper.play_ff(bot, player.id)
        looser_team = teamshelper.get_current_team()
        teamshelper.update_score_other_team()

        winning_team = teamshelper.get_other_team()
        leaderboardhelper.update_users(winning_team.players, settings.POINTS_VICTOIRE)

        blue_team = teamshelper.get_team_by_name('Bleu')
        red_team = teamshelper.get_team_by_name('Rouge')

        await ctx.send(translatehelper.get_team('team_ff', looser_team.name))
        await ctx.send(translatehelper.get_team('blue_team', str(blue_team)))
        await ctx.send(translatehelper.get_team('red_team', str(red_team)))
        await ctx.send(translatehelper.get_roland('restart_roland'))
        state = 'TEAMS'
        # Lancement cartes
        if carteshelper.is_available():
            await ctx.send(translatehelper.get_cards('how_to_start_cards'))

@bot.command(name=LEAD_COMMAND)
async def lead_command(ctx):
    global bot
    if not is_message_valid(ctx):
        return

    username = ctx.author.name
    result = leaderboardhelper.get_user(username)
    if not result:
        leaderboardhelper.insert_user(username, 0)
        result[1] = 0
    await ctx.send(translatehelper.get_lead('score', username, result[1]))

@bot.command(name=LEADERBOARD_COMMAND)
async def leaderboard_command(ctx):
    global bot
    if not is_message_valid(ctx):
        return

    users = leaderboardhelper.get_top_5()
    await ctx.send(translatehelper.get_lead_intro())
    i = 1
    for user in users:
        await ctx.send(translatehelper.get_lead_user(i,user[0], user[1]))
        i+=1

# ----------------------------------------------------------
# ----------------------------------------------------------
# CARTES MYSTERE / PURISTE
# ----------------------------------------------------------
# ----------------------------------------------------------

# Lance une carte mystère ou carte puriste
@bot.command(name=CARDS_COMMAND)
async def cartes_command(ctx):
    global state
    if not is_message_valid(ctx) or state is None:
        return
    loggerhelper.log_command(CARDS_COMMAND, ctx.author)
    await ctx.send(translatehelper.get_cards('card_ad'))
    if state != 'CARTES_SECOND':
        state = "CARTES_FIRST"

# Choix d'une carte mysteres
@bot.command(name=CARD_MYSTERE_COMMAND)
async def mystere_command(ctx):
    global state
    if not is_message_valid(ctx):
        return
    player = ctx.author
    loggerhelper.log_command(CARD_MYSTERE_COMMAND, player)
    if state == 'CARTES_FIRST' or state == 'CARTES_SECOND' and teamshelper.is_player_in_current_team(player.name):
        await vocalhelper.play_mystere(bot, player.id)
        points = await carteshelper.choose_mystere(ctx)
        teamshelper.update_score_current_team(points)
        teamshelper.swap_current_team()
        if state == 'CARTES_FIRST':
            await cartes_command(ctx)
            state = 'CARTES_SECOND'
        else:
            state = 'TEAMS'
            await ctx.send(translatehelper.get_roland('restart_roland'))

# Choix d'une puriste
@bot.command(name=CARD_PURIST_COMMAND)
async def puriste_command(ctx):
    global state
    if not is_message_valid(ctx):
        return
    player = ctx.author
    loggerhelper.log_command(CARD_PURIST_COMMAND, player)
    if state == 'CARTES_FIRST' or state == 'CARTES_SECOND' and teamshelper.is_player_in_current_team(player.name):
        await vocalhelper.play_puriste(bot, player.id)
        await carteshelper.choose_puriste(ctx)

# Reponse a une carte puriste
@bot.command(name=CARD_RESPONSE)
async def puriste_command(ctx, *args):
    global state
    if not is_message_valid(ctx):
        return
    player = ctx.author
    loggerhelper.log_command(CARD_RESPONSE, player)
    if state == 'CARTES_FIRST' or state == 'CARTES_SECOND' and teamshelper.is_player_in_current_team(player.name):
        points = await carteshelper.reponse_puriste(ctx, args[0])
        # Si la reponse est bonne
        if points is not None:
            await vocalhelper.play_win(bot, player.id)
            teamshelper.update_score_current_team(points)
        else:
            await vocalhelper.play_loose(bot, player.id)
        if state == 'CARTES_FIRST':
            teamshelper.swap_current_team()
            state = 'CARTES_SECOND'
            await cartes_command(ctx)
        else:
            state = 'TEAMS'
            await ctx.send(translatehelper.get_roland('restart_roland'))


# ----------------------------------------------------------
# ----------------------------------------------------------
# COMMAND POUR TEST
# ----------------------------------------------------------
# ----------------------------------------------------------


# TEST
@bot.command(name='test')
async def test_command(ctx):
    leaderboardhelper.delete_all()

bot.run(settings.TOKEN_DISCORD)
