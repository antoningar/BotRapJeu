import helpers.filehelper as filehelper
import helpers.spotifyhelper as spotifyhelper
import helpers.translateheper as translatehelper

artists = list()

# recupere le 1er artiste de maniere random
async def get_first_artist(ctx):
    global artists
    # reset de la list dans le cas d'un reroll
    artists = list()
    # recuperation de l'artist
    artist = filehelper.get_random_artists()
    artists.append(artist)
    await ctx.send(translatehelper.get_roland('first_artist',artist))
    
# recuperation du deuxieme artistes et verification du feat
async def get_second_artist(ctx, artist):
    global artists
    # verification que le rappeur n'a pas déjà été cité
    if artist.upper() in [w.upper() for w in artists]:
        await ctx.send(translatehelper.get_roland('rapper_already_played'))
        return
    await ctx.send(translatehelper.get_roland('checking'))
    # verification du feat avec rap genius
    #feat = rapgeniushelper.search(artists[-1], artist)
    # verification du feat avec spotify
    feat = await spotifyhelper.verify(ctx, artists[-1], artist)
    if feat:
        await ctx.send(translatehelper.get_roland('feat_exist',feat))
        artists.append(artist)
        await ctx.send(translatehelper.get_roland('which_feat',artist))
        return 1
    else:
        await ctx.send(translatehelper.get_roland('feat_none'))
