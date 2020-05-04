import discord
from discord.ext import commands

with open("../bot_key.txt") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth]

bot = commands.Bot(command_prefix="!")

channel_id = int(auth[1])

@bot.command()
async def szia(ctx):
    await ctx.send("Szia!")
