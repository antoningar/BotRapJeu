import time
import discord
import random
from discord.errors import ClientException

import helpers.loggerhelper as loggerhelper
import settings

channel = None
client = None
is_muted = True

def set_is_muted(new_muted):
    global is_muted
    is_muted = new_muted

async def set_channel_by_user_id(bot, user_id):
    global channel
    channel = await find_channel_by_user_id(bot, user_id)
    return channel

# Recupere tous les channels du server
# qui sont des channels VOCAUX et qui on AU MOINS DEUX personne de co dessus
def get_channels(bot):
    guild = [x for x in bot.guilds if x.name == settings.GUILD_NAME][0]
    channels = [c for c in guild.channels if 'voice' in c.type and len(c.voice_states) > 0]
    return channels

# Get personnes presente dans le vocal
async def team_player_in_voice(bot, channel, team):
    for voice in channel.voice_states:
        user = await bot.fetch_user(voice)
        user_name = user.name
        if user_name:
            if team.is_player_in_team(user_name):
                return True

async def find_channel_by_user_id(bot, user_id):
    channels = get_channels(bot)
    for channel in channels:
        for voice in channel.voice_states:
            if voice == user_id:
                return channel

# Créer un voice_client
async def start_voice_client(bot, channel):
    global client
    channel = await bot.fetch_channel(channel.id)
    try:
        client = await channel.connect()
    except ClientException as e:
        loggerhelper.log_error('VOCALHELPER', e.msg)
        pass
    return client

# Play un son
async def play(source):
    global client
    client.play(source)
    while client.is_playing():
        time.sleep(1)
    await client.disconnect()

# Tout le processs d'envoi de son
async def play_vocal(bot, vocal):
    global channel
    if is_muted:
        return
    await start_voice_client(bot, channel)
    try:
        source = discord.FFmpegPCMAudio('assets/sons/' + vocal)
    except ClientException as e:
        loggerhelper.log_error('VOCALHELPER', e.msg)
    await play(source)

# Son après un ff
async def play_ff(bot, user_id):
    result = await set_channel_by_user_id(bot, user_id)
    if result is None:
        return
    vocal_possible = [
        "cest_bien_mais_pas_suffisant.mov",
        "très_belle_epreuve.mov"
    ]
    index = random.randrange(len(vocal_possible))
    await play_vocal(bot, vocal_possible[index])

# Son cartes puristes
async def play_puriste(bot, user_id):
    await set_channel_by_user_id(bot, user_id)
    result = await set_channel_by_user_id(bot, user_id)
    if result is None:
        return
    await play_vocal(bot, 'carte_puriste_une_question_sur_le_rap.mov')

# Son cartes mystere
async def play_mystere(bot, user_id):
    result = await set_channel_by_user_id(bot, user_id)
    if result is None:
        return
    await play_vocal(bot, 'carte_mystere_tout_peut_arriver.mov')

# Son lors d'une bonne réponse au roland gamos
async def play_win(bot, user_id):
    result = await set_channel_by_user_id(bot, user_id)
    if result is None:
        return
    vocal_possible = [
        "ca_cest_superbe.mov",
        "ca_me_fait_vibrer.mov",
        "cest_du_jamais_vu_dans_rapjeu.mov",
        "cest_pas_mal_joue.mov",
        "jaccepte_est_ce_quon_a_mieux_ailleur.mov",
        "mais_il_a_du_talent.mov",
        "oh_oui_cest_beau.mov",
        "oui_ouais.mov"
    ]
    index = random.randrange(len(vocal_possible))
    await play_vocal(bot, vocal_possible[index])

# Son lors d'une bonne réponse au roland gamos
async def play_loose(bot, user_id):
    result = await set_channel_by_user_id(bot, user_id)
    if result is None:
        return
    vocal_possible = [
        "les_prenom_de_ta_cousine.mov",
        "jviens_de_vous_arnaquer_je_men_veux.mov",
        "et_jaccepte_les_chanteuse_aussi.mov",
        "cest_bien_mais_pas_suffisant.mov",
        "tu_me_le_dis_si_jtemmerde.mov"
    ]
    index = random.randrange(len(vocal_possible))
    await play_vocal(bot, vocal_possible[index])