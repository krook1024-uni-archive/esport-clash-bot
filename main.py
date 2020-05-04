import coc
import traceback

import discord
from discord.ext import commands

with open("../bot_key.txt") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth]

coc_client = coc.login(auth[2], auth[3], key_count=5, key_names="Bot key", client=coc.EventsClient,)
clan_tag = auth[4]

bot = commands.Bot(command_prefix="!")

channel_id = int(auth[1])

@coc_client.event
async def on_clan_member_versus_trophies_change(old_trophies, new_trophies, player):
    await bot.get_channel(channel_id).send(
        "{0.name}-nek jelenleg {1} versus trófeája van.".format(player, new_trophies))

@bot.command()
async def szia(ctx):
    await ctx.send("Szia!")

@bot.command()
async def hosok(ctx, player_tag):
    try:
        player = await coc_client.get_player(player_tag)
        ret = "{}'s heroes:".format(str(player))
        for hero in player.heroes:
            ret += "{}: level {}/{}".format(str(hero), hero.level, hero.max_level)
        await ctx.send(ret)
    except coc.errors.NotFound:
        await ctx.send("nincs ilyen játékos!")
    except:
        await ctx.send("hiba!")

@bot.command()
async def tagok(ctx):
    try:
        clan = await coc_client.get_clan(clan_tag)
        members = await coc_client.get_members(clan_tag)
        ret = "{} tagjai:\n".format(clan.name)
        for member in members:
            crown = ""
            if member.name == "krook1024": # :P
                crown = "👑"
            ret += "➡  {2}{0}{2} ({1})\n".format(member.name, member.tag, crown)
        await ctx.send(ret)
    except coc.errors.NotFound:
        await ctx.send("nincs ilyen klán!")
    except:
        await ctx.send("hiba!")

coc_client.add_clan_update([clan_tag], retry_interval=60)
coc_client.start_updates()

bot.run(auth[0])
